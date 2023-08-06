import logging
import gc
from typing import List, Tuple, Iterable, Dict, Generator, Callable
import warnings
from collections import OrderedDict, namedtuple, deque

import attr
from attr.validators import instance_of
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from numba import jit, float64, uint64, int64
import h5py
from tqdm import tqdm

from pysight.gui.gui_main import ImagingSoftware
from pysight.nd_hist_generator.line_signal_validators.rectify_lines import LineRectifier
from .frame_chunk import FrameChunk


def trunc_end_of_file(name) -> str:
    """
    Take only the start of the filename to avoid error with Python and Windows

    :param str name: Filename to truncate
    :return str:
    """
    return name[:240]


@attr.s
class Movie:
    """
    Creates FrameChunks that cn be appended into a multi-dimensional movie.

    To create the movie, call the `run()` method. The output will be according to the
    options specified in the GUI, although you can technically override them when
    instantiating this class.

    The Movie object also contains a `show_summed(channel)` method that can will show
    a two-dimensional projection of the multi-dimensional data.

    :param pd.DataFrame data: All recorded data
    :param pd.Series lines: Recorded lines
    :param Generator frame_slices: Slices of frame chunks
    :param pd.Series frames: Recorded frames
    :param float reprate: Laser repetition rate in Hz
    :param str name: Name of the file that is parsed
    :param float binwidth: Binwidth of multiscaler in seconds (100 ps == 100e-12)
    :param float fill_frac: Temporal fill fraction of the original movie, in percentage
    :param bool bidir: Whether the original scan was bi-directional
    :param pd.CategoricalIndex channels: Active and used channels in this iteration
    :param dict outputs: Required outputs
    :param bool censor: Whether to perform censor correction (currently NotImplemented)
    :param bool flim: Whether to perform FLIM
    :param dict lst_metadata: Metadata of the ``.lst`` file
    :param dict exp_params: Parameters used for fitting when using censor correction (currently NotImplemented)
    :param int line_delta: Number of bins between subsequent line signals
    :param bool use_sweeps: Whether to count each sweep as a line in the resulting image
    :param float cache_size: Size of cache in bytes
    :param bool tag_as_phase: Whether to take into consideration the sinusoidal pattern of the TAG lens
    :param float tag_freq: Frequency of TAG lens in Hz
    :param float mirror_phase: Offset phase of the resonant mirror when scanning. If line shift (pixel shift) is
                                observed in the resulting image, change this parameter to fix it
    :param int num_of_frame_chunks: Number of chunks as calculated by the ``VolumeGenerator`` class
    :param int frames_per_chunk: Number of frames inside each chunk. ``frames_per_chunk * num_of_frame_chunks ==
                                len(frames)``
    :param tuple data_shape: Shape of data
    """

    data = attr.ib(validator=instance_of(pd.DataFrame), repr=False)
    lines = attr.ib(validator=instance_of(pd.Series), repr=False)
    frame_slices = attr.ib(repr=False)  # generator of frame slices from VolumeGenerator
    frames = attr.ib(validator=instance_of(pd.Series), repr=False)
    reprate = attr.ib(default=80e6, validator=instance_of(float))
    name = attr.ib(
        default="Movie", validator=instance_of(str), converter=trunc_end_of_file
    )
    binwidth = attr.ib(default=800e-12, validator=instance_of(float))
    fill_frac = attr.ib(default=71.0, validator=instance_of(float))
    bidir = attr.ib(default=False, validator=instance_of(bool))
    channels = attr.ib(
        default=pd.CategoricalIndex([1]), validator=instance_of(pd.CategoricalIndex)
    )
    outputs = attr.ib(factory=dict, validator=instance_of(dict))
    censor = attr.ib(default=False, validator=instance_of(bool))
    flim = attr.ib(default=False, validator=instance_of(bool))
    lst_metadata = attr.ib(factory=dict, validator=instance_of(dict))
    exp_params = attr.ib(factory=dict, validator=instance_of(dict))
    line_delta = attr.ib(default=158_000, validator=instance_of(int))
    use_sweeps = attr.ib(default=False, validator=instance_of(bool))
    cache_size = attr.ib(default=10 * 1024 ** 3, validator=instance_of(int))
    tag_as_phase = attr.ib(default=True, validator=instance_of(bool))
    tag_freq = attr.ib(default=189e3, validator=instance_of(float))
    mirror_phase = attr.ib(default=-2.71, validator=instance_of(float))
    num_of_frame_chunks = attr.ib(default=1, validator=instance_of(int))
    frames_per_chunk = attr.ib(default=1, validator=instance_of(int))
    data_shape = attr.ib(default=(1, 512, 512), validator=instance_of(tuple))
    image_soft = attr.ib(
        default=ImagingSoftware.SCANIMAGE.value, validator=instance_of(str)
    )
    summed_mem = attr.ib(init=False, repr=False)
    stack = attr.ib(init=False, repr=False)
    x_pixels = attr.ib(init=False)
    y_pixels = attr.ib(init=False)
    z_pixels = attr.ib(init=False)
    bins_bet_pulses = attr.ib(init=False)

    def __attrs_post_init__(self):
        self.x_pixels = self.data_shape[1]
        self.y_pixels = self.data_shape[2]
        self.z_pixels = 1
        self.bins_bet_pulses = 1
        if self.flim:
            self.bins_bet_pulses = self.data_shape[-1]
            if len(self.data_shape) == 5:
                self.z_pixels = self.data_shape[3]
        else:
            try:
                self.z_pixels = self.data_shape[3]
            except IndexError:
                pass

    def run(self) -> None:
        """
        Main pipeline for the movie object
        """
        funcs_during, funcs_end = self.__determine_outputs()
        self.__validate_df_indices()
        self.__process_data(funcs_during, funcs_end)
        self.__print_outputs()
        logging.info("Movie object created, analysis done.")

    def __determine_outputs(self) -> Tuple[List[Callable], List[Callable]]:
        """
        Based on the "outputs" variable, decide which outputs to generate.
        Returns a list of pointers to functions to execute for every volume, and after
        finishing generating the entire stack.
        """
        if not self.outputs:
            logging.warning(
                "No outputs requested. Data is still accessible using the dataframe variable."
            )
            return [], []

        funcs_to_execute_during = []
        funcs_to_execute_end = []

        if "memory" in self.outputs:
            self.summed_mem = {i: 0 for i in self.channels}
            self.stack = {i: list() for i in self.channels}
            funcs_to_execute_during.append(self.__create_memory_output)
            funcs_to_execute_end.append(self.__convert_list_to_arr)
            if "stack" in self.outputs:
                funcs_to_execute_end.append(self.__save_stack_at_once)
            if "summed" in self.outputs:
                funcs_to_execute_end.append(self.__save_summed_at_once)

        else:
            if "stack" in self.outputs:
                self.outputs["stack"] = h5py.File(
                    f'{self.outputs["filename"]}',
                    "r+",
                    libver="earliest",
                    rdcc_nbytes=10 * 1024 ** 2,
                    rdcc_nslots=2053,
                    rdcc_w0=1,
                ).require_group("Full Stack")
                funcs_to_execute_during.append(self.__save_stack_incr)
                funcs_to_execute_end.append(self.__close_file)

            if "summed" in self.outputs:
                self.summed_mem = {i: 0 for i in self.channels}
                funcs_to_execute_during.append(self.__append_summed_data)
                funcs_to_execute_end.append(self.__save_summed_at_once)

        return funcs_to_execute_during, funcs_to_execute_end

    def __process_data(
        self, funcs_during: List[Callable], funcs_end: List[Callable]
    ) -> None:
        """
        Create the outputs according to the outputs dictionary.
        Data is generated by appending to a list the needed micro-function to be executed.
        """
        # Execute the appended functions after generating each volume
        tq = tqdm(
            total=self.num_of_frame_chunks,
            desc=f"Processing frame chunks...",
            unit="chunk",
            leave=False,
        )
        for idx, frame_chunk in enumerate(self.frame_slices):
            sliced_df_dict, num_of_frames, frames, lines = self.__slice_df(frame_chunk)
            chunk = FrameChunk(
                movie=self,
                df_dict=sliced_df_dict,
                frames_per_chunk=num_of_frames,
                frames=frames,
                lines=lines,
            )
            hist_dict = chunk.create_hist()
            for func in funcs_during:
                for chan, (hist, _) in hist_dict.items():
                    func(data=hist, channel=chan, idx=idx)

            tq.update(1)
            gc.collect()

        tq.close()
        [func() for func in funcs_end]

    def __slice_df(
        self, frame_chunk
    ) -> Tuple[Dict[int, pd.DataFrame], int, pd.Series, pd.Series]:
        """
        Receives a slice object and slices the DataFrame accordingly -
        once per channel. The returned dictionary has a key for each channel.
        """
        slice_dict = {}
        idx_slice = pd.IndexSlice
        for chan in self.data.index.levels[0].categories:
            slice_dict[chan] = self.data.loc[idx_slice[chan, frame_chunk], :]
        frames = self.frames.loc[frame_chunk]
        num_of_frames = len(frames)
        lines = self.lines.loc[frame_chunk]
        if len(lines) > self.x_pixels * num_of_frames:
            logging.warning(
                f"More-than-necessary line signals in the frame of chunk {frame_chunk}."
            )
        lines = lines.iloc[: self.x_pixels * num_of_frames]
        return slice_dict, num_of_frames, frames, lines

    def __validate_df_indices(self):
        """
        Make sure that the DataFrame of data contains the two
        important indices "Channel" and "Frames", and in the correct order.
        """
        if self.data.index.names[1] == "Lines":
            self.data = self.data.swaplevel()

        assert self.data.index.names[0] == "Channel"
        assert self.data.index.names[1] == "Frames"
        assert self.data.index.names[2] == "Lines"

    def __save_stack_at_once(self) -> None:
        """ Save the entire in-memory stack into .hdf5 file """
        with h5py.File(
            f'{self.outputs["filename"]}',
            "r+",
            libver="earliest",
            rdcc_nbytes=10 * 1024 ** 2,
            rdcc_nslots=2053,
            rdcc_w0=1,
        ) as f:
            logging.info("Saving full stack to disk...")
            for channel in self.channels:
                f["Full Stack"][f"Channel {channel}"][...] = self.stack[channel]

    def __save_summed_at_once(self) -> None:
        """ Save the entire in-memory summed data into .hdf5 file """
        with h5py.File(
            f'{self.outputs["filename"]}',
            "r+",
            libver="earliest",
            rdcc_nbytes=10 * 1024 ** 2,
            rdcc_nslots=2053,
            rdcc_w0=1,
        ) as f:
            for channel in self.channels:
                f["Summed Stack"][f"Channel {channel}"][...] = np.squeeze(
                    self.summed_mem[channel]
                )

    def __close_file(self) -> None:
        """ Close the file pointer of the specific channel """
        self.outputs["stack"].file.close()

    def __convert_list_to_arr(self) -> None:
        """ Convert a list with a bunch of frames into a single numpy array with an extra
        dimension (0) containing the data. There will always be at least one
        frame of time data, this dimension is never squeezed out.
        """
        for channel in self.channels:
            new_stack = np.vstack(self.stack[channel])
            squeezed = np.squeeze(new_stack)
            if (
                new_stack.shape[0] != squeezed.shape[0]
            ):  # a single frame that was squeezed out
                self.stack[channel] = np.expand_dims(squeezed, axis=0)
            else:
                self.stack[channel] = squeezed

    def __create_memory_output(self, data: np.ndarray, channel: int, idx: int) -> None:
        """
        If the user desired, create two memory constructs -
        A summed array of all images (for a specific channel), and a stack containing
        all images in a serial manner.
        :param np.ndarray data: Data to be saved
        :param int channel: Current spectral channel of data
        :param int idx: Index of frame chunk
        """
        self.stack[channel].append(data)
        assert len(data.shape) > 2
        self.summed_mem[channel] += np.uint16(data.sum(axis=0))

    def __save_stack_incr(self, data: np.ndarray, channel: int, idx: int) -> None:
        """
        Save incrementally new data to an open file on the disk
        :param np.ndarray data: Data to save
        :param int channel: Current spectral channel of data
        :param int idx: Index of frame chunk
        """
        cur_slice_start = self.frames_per_chunk * idx
        cur_slice_end = self.frames_per_chunk * (idx + 1)
        self.outputs["stack"][f"Channel {channel}"][
            cur_slice_start:cur_slice_end, ...
        ] = np.squeeze(data)

    def __append_summed_data(self, data: np.ndarray, channel: int, idx: int) -> None:
        """
        Create a summed variable later to be saved as the channel's data
        :param np.ndarray data: Data to be saved
        :param int channel: Spectral channel of data to be saved
        :param int idx: Index of frame chunk
        """
        assert len(data.shape) > 2
        self.summed_mem[channel] += np.uint16(data.sum(axis=0))

    def __print_outputs(self) -> None:
        """ Print to console the outputs that were generated. """
        if not self.outputs:
            return

        logging.info(
            "======================================================= \nOutputs:\n--------"
        )
        if "stack" in self.outputs:
            logging.info(
                f'Stack file created with name "{self.outputs["filename"]}", \ncontaining a data group named'
                ' "Full Stack", with one dataset per channel.'
            )

        if "memory" in self.outputs:
            logging.info(
                "The full data is present in dictionary form (key per channel) under `movie.stack`, "
                "and in stacked form under `movie.summed_mem`."
            )

        if "summed" in self.outputs:
            logging.info(
                f'Summed stack file created with name "{self.outputs["filename"]}", \ncontaining a data group named'
                ' "Summed Stack", with one dataset per channel.'
            )

    def __nano_flim(self, data: np.ndarray) -> None:
        pass

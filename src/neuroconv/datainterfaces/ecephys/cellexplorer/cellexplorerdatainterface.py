from pathlib import Path
from typing import Literal, Optional

import numpy as np
import scipy
from pynwb import NWBFile

from ..baserecordingextractorinterface import BaseRecordingExtractorInterface
from ..basesortingextractorinterface import BaseSortingExtractorInterface
from ....tools import get_package
from ....utils import FilePathType


class CellExplorerRecordingInterface(BaseRecordingExtractorInterface):
    """
    This interface serves as an temporary solution for integrating CellExplorer metadata during a conversion process.

    CellExplorer's new format (https://cellexplorer.org/) contains a `session.mat` file, which has the following field:

    * Sampling frequency
    * Gains for both raw data (held in a file named session.dat) and lfp (located in session.lfp)
    * Dtype for both raw data and lfp.

    Link to the documentation detailing the file's structure:
    https://cellexplorer.org/datastructure/data-structure-and-format/#session-metadata

    If the binary file is available (session.dat), the interface will use the `BinaryRecordingExtractor` to load the
    data. Otherwise, it will use the `NumpyRecording` extractor, which is a dummy extractor that only contains
    metadata. This can be used to add the electrode using `write_electrical_series=False` as a conversion option.

    In its current form, the `chanMap.mat` file is employed to extract the electrode coordinates within the probe.
    To my understanding, this file is generated for using kilosort, and it is not granted that it will
    be universally available for all future conversion projects. Ideally, the format should also contain
    files for channel info and channel coordinates, although these are absent in the current conversion:

    https://cellexplorer.org/datastructure/data-structure-and-format/#channels

    As we accumulate more examples moving forward, we will be able to figure out what's better. This is a first
    iteration.
    """

    sampling_frequency_key = "sr"
    binary_file_extension = "dat"

    def __init__(self, folder_path, verbose=True, es_key: str = "ElectricalSeries"):
        self.folder_path = Path(folder_path)

        # No super here, we need to do everything by hand
        self.verbose = verbose
        self.es_key = es_key
        self.subset_channels = None
        self.source_data = dict(folder_path=folder_path)

        self.session = self.folder_path.name

        session_data_file_path = self.folder_path / f"{self.session}.session.mat"
        assert session_data_file_path.is_file(), f"File {session_data_file_path} does not exist"

        from pymatreader import read_mat

        ignore_fields = ["animal", "behavioralTracking", "timeSeries", "spikeSorting", "epochs"]
        session_data = read_mat(filename=session_data_file_path, ignore_fields=ignore_fields)["session"]
        extracellular_data = session_data["extracellular"]

        num_channels = int(extracellular_data["nChannels"])
        gain = float(extracellular_data["leastSignificantBit"])  # 0.195
        gains_to_uv = np.ones(num_channels) * gain
        dtype = np.dtype(extracellular_data["precision"])
        sampling_frequency = float(extracellular_data[self.sampling_frequency_key])

        binary_file_path = self.folder_path / f"{self.session}.{self.binary_file_extension}"
        if binary_file_path.is_file():
            from spikeinterface.core.binaryrecordingextractor import (
                BinaryRecordingExtractor,
            )

            self.recording_extractor = BinaryRecordingExtractor(
                file_paths=[binary_file_path],
                sampling_frequency=sampling_frequency,
                num_chan=num_channels,
                dtype=dtype,
                t_starts=None,
                file_offset=0,
                gain_to_uV=gains_to_uv,
                offset_to_uV=None,
            )
        else:
            from spikeinterface.core.numpyextractors import NumpyRecording

            channel_ids = None
            traces_list = [np.empty(shape=(1, num_channels))]
            dummy_recording = NumpyRecording(
                traces_list=traces_list,
                sampling_frequency=sampling_frequency,
                channel_ids=channel_ids,
            )

            self.recording_extractor = dummy_recording
            self.recording_extractor.set_channel_gains(channel_ids=channel_ids, gains=np.ones(num_channels) * gain)

        self.chan_map_file_path = self.folder_path / f"chanMap.mat"
        if self.chan_map_file_path.is_file():
            channel_map_data = read_mat(self.chan_map_file_path)
            channel_groups = channel_map_data["connected"]
            channel_group_names = [f"Group{group_index + 1}" for group_index in channel_groups]

            channel_indices = channel_map_data["chanMap0ind"]
            channel_ids = [str(channel_indices[i]) for i in channel_indices]
            channel_name = [
                f"ch{channel_index}grp{channel_group}"
                for channel_index, channel_group in zip(channel_indices, channel_groups)
            ]
            base_ids = self.recording_extractor.get_channel_ids()
            self.recording_extractor = self.recording_extractor.channel_slice(
                channel_ids=base_ids, renamed_channel_ids=channel_ids
            )
            x_coords = channel_map_data["xcoords"]
            y_coords = channel_map_data["ycoords"]
            locations = np.array((x_coords, y_coords)).T.astype("float32")
            self.recording_extractor.set_channel_locations(channel_ids=channel_ids, locations=locations)

            self.recording_extractor.set_property(key="channel_name", values=channel_name)
            self.recording_extractor.set_property(key="group", ids=channel_ids, values=channel_groups)
            self.recording_extractor.set_property(key="group_name", ids=channel_ids, values=channel_group_names)

        self._number_of_segments = self.recording_extractor.get_num_segments()


class CellExplorerLFPInterface(CellExplorerRecordingInterface):
    keywords = BaseRecordingExtractorInterface.keywords + [
        "extracellular electrophysiology",
        "LFP",
        "local field potential",
        "LF",
    ]

    sampling_frequency_key = "srLfp"
    binary_file_extension = "lfp"

    def __init__(self, folder_path, verbose=True, es_key: str = "ElectricalSeriesLFP"):
        super().__init__(folder_path, verbose, es_key)

    def add_to_nwbfile(
        self,
        nwbfile: NWBFile,
        metadata: Optional[dict] = None,
        stub_test: bool = False,
        starting_time: Optional[float] = None,
        write_as: Literal["raw", "lfp", "processed"] = "lfp",
        write_electrical_series: bool = True,
        compression: Optional[str] = None,
        compression_opts: Optional[int] = None,
        iterator_type: str = "v2",
        iterator_opts: Optional[dict] = None,
    ):
        return super().add_to_nwbfile(
            nwbfile,
            metadata,
            stub_test,
            starting_time,
            write_as,
            write_electrical_series,
            compression,
            compression_opts,
            iterator_type,
            iterator_opts,
        )


class CellExplorerSortingInterface(BaseSortingExtractorInterface):
    """Primary data interface class for converting Cell Explorer spiking data."""

    def __init__(self, file_path: FilePathType, verbose: bool = True):
        """
        Initialize read of Cell Explorer file.

        Parameters
        ----------
        file_path: FilePathType
            Path to .spikes.cellinfo.mat file.
        verbose: bool, default: True
        """

        hdf5storage = get_package(package_name="hdf5storage")

        super().__init__(spikes_matfile_path=file_path, verbose=verbose)
        self.source_data = dict(file_path=file_path)
        spikes_matfile_path = Path(file_path)

        session_path = Path(file_path).parent
        session_id = session_path.stem

        assert (
            spikes_matfile_path.is_file()
        ), f"The file_path should point to an existing .spikes.cellinfo.mat file ({spikes_matfile_path})"

        try:
            spikes_mat = scipy.io.loadmat(file_name=str(spikes_matfile_path))
            self.read_spikes_info_with_scipy = True
        except NotImplementedError:
            spikes_mat = hdf5storage.loadmat(file_name=str(spikes_matfile_path))
            self.read_spikes_info_with_scipy = False
        cell_info = spikes_mat.get("spikes", np.empty(0))
        self.cell_info_fields = cell_info.dtype.names

        unit_ids = self.sorting_extractor.get_unit_ids()
        if self.read_spikes_info_with_scipy:
            if "cluID" in self.cell_info_fields:
                self.sorting_extractor.set_property(
                    ids=unit_ids, key="clu_id", values=[int(x) for x in cell_info["cluID"][0][0][0]]
                )
            if "shankID" in self.cell_info_fields:
                self.sorting_extractor.set_property(
                    ids=unit_ids, key="group_id", values=[f"Group{x}" for x in cell_info["shankID"][0][0][0]]
                )
            if "region" in self.cell_info_fields:
                self.sorting_extractor.set_property(
                    ids=unit_ids, key="location", values=[str(x[0]) for x in cell_info["region"][0][0][0]]
                )
        else:  # Logic for hdf5storage
            if "cluID" in self.cell_info_fields:
                self.sorting_extractor.set_property(
                    ids=unit_ids, key="clu_id", values=[int(x) for x in cell_info["cluID"][0][0]]
                )
            if "shankID" in self.cell_info_fields:
                self.sorting_extractor.set_property(
                    ids=unit_ids, key="group_id", values=[f"Group{x}" for x in cell_info["shankID"][0][0]]
                )
            if "region" in self.cell_info_fields:
                self.sorting_extractor.set_property(
                    ids=unit_ids, key="location", values=[str(x[0]) for x in cell_info["region"][0][0]]
                )
        celltype_mapping = {"pE": "excitatory", "pI": "inhibitory", "[]": "unclassified"}
        celltype_file_path = session_path / f"{session_id}.CellClass.cellinfo.mat"
        if celltype_file_path.is_file():
            celltype_info = scipy.io.loadmat(celltype_file_path).get("CellClass", np.empty(0))
            if "label" in celltype_info.dtype.names:
                self.sorting_extractor.set_property(
                    ids=unit_ids,
                    key="cell_type",
                    values=[str(celltype_mapping[str(x[0])]) for x in celltype_info["label"][0][0][0]],
                )

    def get_metadata(self) -> dict:
        metadata = super().get_metadata()
        session_path = Path(self.source_data["file_path"]).parent
        session_id = session_path.stem
        # TODO: add condition for retrieving ecephys metadata if no recording or lfp are included in conversion
        metadata["NWBFile"].update(session_id=session_id)

        unit_properties = []
        cellinfo_file_path = session_path / f"{session_id}.spikes.cellinfo.mat"
        if cellinfo_file_path.is_file():
            cell_info_fields = self.cell_info_fields
            if "cluID" in cell_info_fields:
                unit_properties.append(
                    dict(
                        name="clu_id",
                        description="0-indexed id of cluster identified from the shank.",
                    )
                )
            if "shankID" in cell_info_fields:
                unit_properties.append(
                    dict(
                        name="group_id",
                        description="The electrode group ID that each unit was identified by.",
                    )
                )
            if "region" in cell_info_fields:
                unit_properties.append(
                    dict(
                        name="location",
                        description="Brain region where each unit was detected.",
                    )
                )
        celltype_filepath = session_path / f"{session_id}.CellClass.cellinfo.mat"
        if celltype_filepath.is_file():
            celltype_info = scipy.io.loadmat(celltype_filepath).get("CellClass", np.empty(0))
            if "label" in celltype_info.dtype.names:
                unit_properties.append(
                    dict(
                        name="cell_type",
                        description="Type of cell this has been classified as.",
                    )
                )
        metadata.update(Ecephys=dict(UnitProperties=unit_properties))
        return metadata

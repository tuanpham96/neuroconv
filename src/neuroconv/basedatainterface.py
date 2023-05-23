import uuid
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional

from pynwb import NWBFile

from .tools.nwb_helpers import make_or_load_nwbfile
from .utils import get_schema_from_method_signature, load_dict_from_file
from .utils.dict import DeepDict


class BaseDataInterface(ABC):
    """Abstract class defining the structure of all DataInterfaces."""

    keywords: List[str] = []

    @classmethod
    def get_source_schema(cls):
        """Infer the JSON schema for the source_data from the method signature (annotation typing)."""
        return get_schema_from_method_signature(cls, exclude=["source_data"])

    def __init__(self, **source_data):
        self.source_data = source_data

    def get_conversion_options_schema(self):
        """Infer the JSON schema for the conversion options from the method signature (annotation typing)."""
        return get_schema_from_method_signature(self.run_conversion, exclude=["nwbfile", "metadata"])

    def get_metadata_schema(self):
        """Retrieve JSON schema for metadata."""
        metadata_schema = load_dict_from_file(Path(__file__).parent / "schemas" / "base_metadata_schema.json")
        return metadata_schema

    def get_metadata(self):
        """Child DataInterface classes should override this to match their metadata."""
        metadata = DeepDict()
        metadata["NWBFile"]["session_description"] = "Auto-generated by neuroconv"
        metadata["NWBFile"]["identifier"] = str(uuid.uuid4())

        return metadata

    def add_to_nwbfile(self, nwbfile: NWBFile, **conversion_options):
        raise NotImplementedError()

    @abstractmethod
    def run_conversion(
        self,
        nwbfile_path: Optional[str] = None,
        nwbfile: Optional[NWBFile] = None,
        metadata: Optional[dict] = None,
        overwrite: bool = False,
        **conversion_options,
    ):
        """
        Run the NWB conversion for the instantiated data interface.

        Parameters
        ----------
        nwbfile_path : FilePathType
            Path for where to write or load (if overwrite=False) the NWBFile.
            If specified, the context will always write to this location.
        nwbfile : NWBFile, optional
            An in-memory NWBFile object to write to the location.
        metadata : dict, optional
            Metadata dictionary with information used to create the NWBFile when one does not exist or overwrite=True.
        overwrite : bool, default: False
            Whether to overwrite the NWBFile if one exists at the nwbfile_path.
            The default is False (append mode).
        """

        with make_or_load_nwbfile(
            nwbfile_path=nwbfile_path,
            nwbfile=nwbfile,
            metadata=metadata,
            overwrite=overwrite,
        ) as nwbfile:
            self.add_to_nwbfile(nwbfile, **conversion_options)

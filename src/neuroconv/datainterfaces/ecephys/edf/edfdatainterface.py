"""Authors: Heberto Mayorquin"""
from spikeinterface.extractors import EDFRecordingExtractor
from ..baserecordingextractorinterface import BaseRecordingExtractorInterface

from ....utils.types import FilePathType

try:
    import pyedflib

    HAVE_PYEDFLIB = True
except ImportError:
    HAVE_PYEDFLIB = False
INSTALL_MESSAGE = "Please install pyedflib (https://pypi.org/project/pyEDFlib/) to use this interface!"


class EDFRecordingInterface(BaseRecordingExtractorInterface):
    """Primary data interface class for converting European Data Format (EDF) data."""

    RX = EDFRecordingExtractor

    def __init__(self, file_path: FilePathType, verbose: bool = True):
        """
        Load and prepare sorting data for kilosort

        Parameters
        ----------
        folder_path: str or Path
            Path to the edf file
        verbose: bool, True by default
            Allows verbose.
        """
        super().__init__(file_path=file_path, verbose=verbose)

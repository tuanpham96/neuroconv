import json
from dateutil.parser import parse as dateparse
from typing import Optional

from roiextractors import ScanImageTiffImagingExtractor

try:
    from ScanImageTiffReader import ScanImageTiffReader

    HAVE_SCAN_IMAGE_TIFF = True
except ImportError:
    HAVE_SCAN_IMAGE_TIFF = False


from ..baseimagingextractorinterface import BaseImagingExtractorInterface
from ....utils import FilePathType


def extract_extra_metadata(file_path):

    description = ScanImageTiffReader(str(file_path)).description(iframe=0)
    extra_metadata = {x.split("=")[0]: x.split("=")[1] for x in description.split("\r") if "=" in x}

    return extra_metadata


from PIL import Image, ExifTags


def extract_extra_metadata2(file_path):
    image = Image.open(file_path)
    image_exif = image.getexif()
    exif = {ExifTags.TAGS[k]: v for k, v in image_exif.items() if k in ExifTags.TAGS and type(v) is not bytes}
    extra_metadata = {x.split("=")[0]: x.split("=")[1] for x in exif["ImageDescription"].split("\r") if "=" in x}

    return extra_metadata


class ScanImageImagingInterface(BaseImagingExtractorInterface):

    IX = ScanImageTiffImagingExtractor

    @classmethod
    def get_source_schema(cls):
        source_schema = super().get_source_schema()
        source_schema["properties"]["file_path"]["description"] = "Path to Tiff file."
        return source_schema

    def __init__(
        self,
        file_path: FilePathType,
        fallback_sampling_frequency: Optional[float] = None,
    ):
        """
        DataInterface for reading Tiff files that are generated by ScanImage. This interface extracts the metadata
        from the exif of the tiff file.

        Parameters
        ----------
        file_path: str
            Path to tiff file.
        fallback_sampling_frequency: float, optional
            The sampling frequency can usually be extracted from the scanimage metadata in
            exif:ImageDescription:state.acq.frameRate. If not, use this.
        """

        assert (
            HAVE_SCAN_IMAGE_TIFF
        ), "To use the ScanImageTiffExtractor install scanimage-tiff-reader: \n\n pip install scanimage-tiff-reader\n\n"
        self.image_metadata = extract_extra_metadata(file_path=file_path)

        if "state.acq.frameRate" in self.image_metadata:
            sampling_frequency = float(self.image_metadata["state.acq.frameRate"])
        else:
            assert_msg = (
                "sampling frequency not found in image metadata, "
                "input the frequency using the argument `fallback_sampling_frequency`"
            )
            assert fallback_sampling_frequency is not None, assert_msg
            sampling_frequency = fallback_sampling_frequency

        super().__init__(file_path=file_path, sampling_frequency=sampling_frequency)

    def get_metadata(self):
        device_number = 0  # Imaging plane metadata is a list with metadata for each plane

        metadata = super().get_metadata()

        if "state.internal.triggerTimeString" in self.image_metadata:
            extracted_session_start_time = dateparse(self.image_metadata["state.internal.triggerTimeString"])
            metadata["NWBFile"] = dict(session_start_time=extracted_session_start_time)

        # Extract many scan image properties and attach them as dic in the description
        ophys_metadata = metadata["Ophys"]
        two_photon_series_metadata = ophys_metadata["TwoPhotonSeries"][device_number]
        if self.image_metadata is not None:
            extracted_description = json.dumps(self.image_metadata)
            two_photon_series_metadata.update(description=extracted_description)

        return metadata

from pathlib import Path

import numpy as np
from openeo.rest.connection import Connection
from openeo.rest.job import JobFailedException

from .utils import Parameters


def main(conn: Connection, in_path: Path, parameters: Parameters) -> None:
    """
    Connects to openeo and downloads a yearly mosaic over a test area.
    Requires the environment variable "TEST_PATH" which should point to a test directory.
    Variables for the test will be stored there.
    """

    print("Start setup for downloading data")
    save_path = in_path / "openeo_tifs"
    save_path.mkdir(exist_ok=True)

    # Openeo processing, currently hard set values for a test area
    dc = conn.load_collection(
        "SENTINEL2_L2A",
        spatial_extent=parameters.SPATIAL_EXTENT,
        temporal_extent=parameters.TEMP_EXTENT,
        bands=parameters.BANDS + ["CLD", "SCL", "B11"],
        max_cloud_cover=parameters.MAX_CLOUD_COVER,
    )

    # load_collection does not actually filter spatially, contrary to its documentation
    # so we need to filter spatially manually if more specific (than bbox) geometry is given
    if not parameters.SPATIAL_EXTENT.get("west"):
        # We assume we have a valid geojson extent, and not just a bbox
        dc = dc.filter_spatial(parameters.SPATIAL_EXTENT)

    try:
        dc = apply_cm(dc)
        dc = dc.filter_bands(parameters.BANDS)
        dc.save_result(format="GTiff")
        job = dc.create_job()

        print("Start execute_batch data-download")
        job.start_and_wait()
        results = job.get_results()
        results.download_files(save_path)
    except JobFailedException as e:
        print("Openeo job failed. There might be no scene available.")
        print(f"Error message: {e}")
        raise


def apply_cm(dc, ks: int = 5):
    """
    Applies cloud masking to an openeo cube.

    Parameters
    ----------
    ks : int, optional
        Kernel size for cloud buffering, by default 5
    """
    kernel = np.ones((ks, ks), dtype=int)
    cm = (
        (dc.band("CLD") >= 80)
        | (dc.band("SCL") == 8)
        | (dc.band("SCL") == 9)
        | (dc.band("SCL") == 10)
    )
    # Dilation (expand mask)
    dilated = cm.apply_kernel(kernel)
    dilated = dilated > 0
    dc = dc.mask(dilated)

    dc = dc.mask((dc.band("SCL") == 2) | (dc.band("SCL") == 3) | (dc.band("SCL") == 4))

    swir_mask = dc.band("B11") > 250
    swir_mask = swir_mask.apply_kernel(kernel)
    swir_mask = swir_mask > 0
    swir_mask = swir_mask.apply_kernel(kernel)
    swir_mask = swir_mask == ks**2

    dc = dc.mask(swir_mask)

    return dc

import os
import tempfile
from pathlib import Path
from typing import Dict

from openeo.rest.connection import Connection
from pystac import Catalog

from .openeo import main as download
from .postprocess import main as postprocess
from .utils import Parameters


class Algorithm:

    @staticmethod
    def run(conn: Connection, catalog: Catalog, parameters: Dict) -> None:
        """
        Entrypoint for all runnable Algorithms.

        :param conn: openEO-Connection, already pre-authenticated
        :param catalog: STAC-Catalog storing all outputs this algorithm produces
        :param parameters: User-Supplied parameters.
        :return: None
        """
        os.chdir(Path(__file__).resolve().parent)

        try:
            # Set some sane default parameters
            BANDS = parameters.get("bands") or ["B02", "B03", "B04", "B08"]
            if (parameters.get("rangestart") and parameters.get("rangeend")):
                TEMP_EXTENT = (parameters.get("rangestart"), parameters.get("rangeend"))
            else:
                TEMP_EXTENT = ("2023-01-01", "2023-02-10")
            SPATIAL_EXTENT = parameters.get("spatial_extent") or {
                "west": 118.54074,
                "south": 4.31173,
                "east": 118.58351,
                "north": 4.34025,
                "crs": "EPSG:4326",
            }
            MAX_CLOUD_COVER = parameters.get("maxcloudcover")

            params = Parameters(BANDS, TEMP_EXTENT, SPATIAL_EXTENT, MAX_CLOUD_COVER)
            print(f"Running with parameters {params}")

            with tempfile.TemporaryDirectory(delete=False) as workdir:
                print(f"Triggering download")
                download(conn, Path(workdir), params)

                print(f"Triggering postprocess")
                postprocess(Path(workdir),
                        Path(Path(__file__).resolve().parent) / "models",
                        catalog)

        except Exception as e:
            # TODO: improve error logging
            print(e)

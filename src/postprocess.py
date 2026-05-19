import argparse
import os
import pickle
import urllib.request
from pathlib import Path
from tempfile import TemporaryDirectory
import json

import rasterio
import pystac
from pystac import Catalog
from pystac.extensions.eo import Band, EOExtension
from pystac.extensions.projection import ProjectionExtension
from pystac.extensions.view import ViewExtension
import shapely
from shapely.geometry import box
from shapely.geometry import Polygon, mapping
from datetime import datetime, timezone


def main(work_dir: Path, catalog: Catalog) -> None:

    tif_dir = work_dir / "openeo_tifs"

    # Just work on the first file
    files = list(tif_dir.glob("*.tif"))

    if len(files) > 0:
        file_path = files[0]

        print(f"Working on File: {file_path}")
        # Get original crs
        with rasterio.open(file_path) as r:
            crs = r.crs
            bounds = r.bounds
            bbox = [bounds.left, bounds.bottom, bounds.right, bounds.top]
            footprint = Polygon([
                [bounds.left, bounds.bottom],
                [bounds.left, bounds.top],
                [bounds.right, bounds.top],
                [bounds.right, bounds.bottom]
            ])

            metadata = {"epsg": "32650"}

            item_id = file_path.name

            # resolve the datetime in the semantics of STAC (-> time for data coverage ~= sampling time)
            dt = datetime.now(tz=timezone.utc) # default fallback
            item_id_wo_ext = item_id.split(".")[0]
            if ("_" in item_id_wo_ext):
                chunks = item_id_wo_ext.split("_")
                for c in chunks:
                    print(f"parsing datetime from: {c[:10]}")
                    try:
                        dt = datetime.fromisoformat(c[:10])
                        break
                    except ValueError:
                        pass

            item = pystac.Item(id=item_id,
                               geometry=json.loads(shapely.to_geojson(footprint)),
                               bbox=bbox,
                               datetime=dt,
                               properties=metadata)

            item.add_asset(
                key='image',
                asset=pystac.Asset(
                    href=file_path.as_posix(),
                    media_type=pystac.MediaType.GEOTIFF
                ))
            
            catalog.add_item(item)
        
        print("Created catalog:")
        catalog.describe()

    else:
        print("No tif file found.")

if __name__ == "__main__":
    try:
        work_dir = Path(os.environ["TEST_PATH"])
    except KeyError:
        raise RuntimeError("TEST_PATH environment variable must be set.")
    main(work_dir, work_dir)

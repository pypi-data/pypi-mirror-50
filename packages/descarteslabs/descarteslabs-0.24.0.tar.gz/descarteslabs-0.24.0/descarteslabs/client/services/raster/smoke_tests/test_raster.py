# Copyright 2018-2019 Descartes Labs.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import tempfile
import shutil
import unittest
import json
import mock

import descarteslabs.client.addons as addons
from descarteslabs.client.addons import numpy as np
from descarteslabs.client.services.raster import Raster
import descarteslabs.client.services.raster.raster

from descarteslabs.client.services.raster.smoke_tests.iowa_geometry import iowa_geom


class TestRaster(unittest.TestCase):
    raster = None
    places = None

    @classmethod
    def setUpClass(cls):
        cls.raster = Raster()

    def test_raster(self):
        # TODO: Remove key test once keys are deprecated and removed.
        # test with scene key
        r = self.raster.raster(
            inputs=["landsat:LC08:PRE:TOAR:meta_LC80270312016188_v1"],
            bands=["red", "green", "blue", "alpha"],
            resolution=960,
        )
        self.assertTrue("metadata" in r)
        self.assertTrue("files" in r)
        self.assertTrue(
            "landsat:LC08:PRE:TOAR:meta_LC80270312016188_v1_red-green-blue-alpha.tif"
            in r["files"]
        )

        # test with scene id
        r = self.raster.raster(
            inputs=["landsat:LC08:PRE:TOAR:meta_LC80270312016188_v1"],
            bands=["red", "green", "blue", "alpha"],
            resolution=960,
        )
        self.assertTrue("metadata" in r)
        self.assertTrue("files" in r)
        self.assertTrue(
            "landsat:LC08:PRE:TOAR:meta_LC80270312016188_v1_red-green-blue-alpha.tif"
            in r["files"]
        )

    def test_raster_save(self):
        tmpdir = tempfile.mkdtemp()
        try:
            response = self.raster.raster(
                inputs=["landsat:LC08:PRE:TOAR:meta_LC80270312016188_v1"],
                bands=["red", "green", "blue", "alpha"],
                resolution=960,
                save=True,
                outfile_basename="{}/my-raster".format(tmpdir),
            )
            with open("{}/my-raster.tif".format(tmpdir), "rb") as f:
                f.seek(0, os.SEEK_END)
                length = f.tell()
            self.assertEqual(
                length, len(response["files"]["{}/my-raster.tif".format(tmpdir)])
            )
        finally:
            shutil.rmtree(tmpdir)

    def test_ndarray(self):
        data, metadata = self.raster.ndarray(
            inputs=["landsat:LC08:PRE:TOAR:meta_LC80270312016188_v1"],
            bands=["red", "green", "blue", "alpha"],
            resolution=960,
        )
        self.assertEqual(data.shape, (249, 245, 4))
        self.assertEqual(data.dtype, np.uint16)
        self.assertEqual(len(metadata["bands"]), 4)

    def test_ndarray_single_band(self):
        data, metadata = self.raster.ndarray(
            inputs=["landsat:LC08:PRE:TOAR:meta_LC80270312016188_v1"],
            bands=["red"],
            resolution=960,
        )
        self.assertEqual(data.shape, (249, 245))
        self.assertEqual(data.dtype, np.uint16)
        self.assertEqual(len(metadata["bands"]), 1)

    def test_ndarray_no_blosc(self):
        args = dict(
            inputs=["landsat:LC08:PRE:TOAR:meta_LC80270312016188_v1"],
            bands=["red", "green", "blue", "alpha"],
            resolution=960,
            align_pixels=True,
        )
        r, meta = self.raster.ndarray(**args)

        with mock.patch.object(
            descarteslabs.client.services.raster.raster,
            "blosc",
            addons.ThirdParty("blosc"),
        ):
            r2, meta2 = self.raster.ndarray(**args)

        np.testing.assert_array_equal(r, r2)
        self.assertEqual(meta, meta2)

    def test_stack_dltile(self):
        dltile = "128:16:960.0:15:-2:37"
        keys = [
            "landsat:LC08:PRE:TOAR:meta_LC80270312016188_v1",
            "landsat:LC08:PRE:TOAR:meta_LC80260322016197_v1",
        ]

        stack, metadata = self.raster.stack(
            keys, dltile=dltile, bands=["red", "green", "blue", "alpha"]
        )
        self.assertEqual(stack.shape, (2, 160, 160, 4))
        self.assertEqual(stack.dtype, np.uint16)
        self.assertEqual(len(metadata), 2)
        self.assertNotEqual(metadata[0], metadata[1])

    def test_stack_dltile_gdal_order(self):
        dltile = "128:16:960.0:15:-2:37"
        keys = [
            "landsat:LC08:PRE:TOAR:meta_LC80270312016188_v1",
            "landsat:LC08:PRE:TOAR:meta_LC80260322016197_v1",
        ]

        stack, metadata = self.raster.stack(
            keys, dltile=dltile, bands=["red", "green", "blue", "alpha"], order="gdal"
        )
        self.assertEqual(stack.shape, (2, 4, 160, 160))
        self.assertEqual(stack.dtype, np.uint16)
        self.assertEqual(len(metadata), 2)
        self.assertNotEqual(metadata[0], metadata[1])

    def test_stack_one_image(self):
        dltile = "128:16:960.0:15:-2:37"
        keys = ["landsat:LC08:PRE:TOAR:meta_LC80270312016188_v1"]

        stack, metadata = self.raster.stack(
            keys, dltile=dltile, bands=["red", "green", "blue", "alpha"]
        )
        self.assertEqual(stack.shape, (1, 160, 160, 4))
        self.assertEqual(stack.dtype, np.uint16)
        self.assertEqual(len(metadata), 1)

    def test_stack_one_band(self):
        dltile = "128:16:960.0:15:-2:37"
        keys = ["landsat:LC08:PRE:TOAR:meta_LC80270312016188_v1"]

        stack, metadata = self.raster.stack(keys, dltile=dltile, bands=["red"])
        self.assertEqual(stack.shape, (1, 160, 160, 1))
        self.assertEqual(stack.dtype, np.uint16)
        self.assertEqual(len(metadata), 1)

    def test_stack_one_band_gdal_order(self):
        dltile = "128:16:960.0:15:-2:37"
        keys = ["landsat:LC08:PRE:TOAR:meta_LC80270312016188_v1"]

        stack, metadata = self.raster.stack(
            keys, dltile=dltile, bands=["red"], order="gdal"
        )
        self.assertEqual(stack.shape, (1, 1, 160, 160))
        self.assertEqual(stack.dtype, np.uint16)

    def test_stack_res_cutline_utm(self):
        geom = {
            "coordinates": (
                (
                    (-95.66055514862535, 41.24469400862013),
                    (-94.74931826062456, 41.26199387228942),
                    (-94.76311013534223, 41.95357639323731),
                    (-95.69397431605952, 41.93542085595837),
                    (-95.66055514862535, 41.24469400862013),
                ),
            ),
            "type": "Polygon",
        }
        keys = [
            "landsat:LC08:PRE:TOAR:meta_LC80270312016188_v1",
            "landsat:LC08:PRE:TOAR:meta_LC80260322016197_v1",
        ]
        resolution = 960
        stack, metadata = self.raster.stack(
            keys,
            resolution=resolution,
            cutline=geom,
            srs="EPSG:32615",
            bounds=(277280.0, 4569600.0, 354080.0, 4646400.0),
            bands=["red", "green", "blue", "alpha"],
        )
        self.assertEqual(stack.shape, (2, 80, 80, 4))
        self.assertEqual(stack.dtype, np.uint16)

    def test_stack_res_cutline_wgs84(self):
        geom = {
            "coordinates": (
                (
                    (-95.66055514862535, 41.24469400862013),
                    (-94.74931826062456, 41.26199387228942),
                    (-94.76311013534223, 41.95357639323731),
                    (-95.69397431605952, 41.93542085595837),
                    (-95.66055514862535, 41.24469400862013),
                ),
            ),
            "type": "Polygon",
        }
        keys = [
            "landsat:LC08:PRE:TOAR:meta_LC80270312016188_v1",
            "landsat:LC08:PRE:TOAR:meta_LC80260322016197_v1",
        ]
        resolution = 960
        stack, metadata = self.raster.stack(
            keys,
            resolution=resolution,
            cutline=geom,
            srs="EPSG:32615",
            bounds=(
                -95.69397431605952,
                41.24469400862013,
                -94.74931826062456,
                41.95357639323731,
            ),
            bounds_srs="EPSG:4326",
            bands=["red", "green", "blue", "alpha"],
        )
        self.assertEqual(stack.shape, (2, 80, 84, 4))
        self.assertEqual(stack.dtype, np.uint16)

    def test_cutline_dict(self):
        shape = {
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-95.2989209, 42.7999878],
                        [-93.1167728, 42.3858464],
                        [-93.7138666, 40.703737],
                        [-95.8364984, 41.1150618],
                        [-95.2989209, 42.7999878],
                    ]
                ],
            }
        }
        try:
            data, metadata = self.raster.ndarray(
                inputs=["landsat:LC08:PRE:TOAR:meta_LC80270312016188_v1"],
                bands=["red"],
                resolution=960,
                cutline=shape,
            )
            self.assertEqual(data.shape, (245, 238))
            self.assertEqual(data.dtype, np.uint16)
            self.assertEqual(len(metadata["bands"]), 1)
        except ImportError:
            pass

    def test_cutline_str(self):
        shape = {
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-95.2989209, 42.7999878],
                        [-93.1167728, 42.3858464],
                        [-93.7138666, 40.703737],
                        [-95.8364984, 41.1150618],
                        [-95.2989209, 42.7999878],
                    ]
                ],
            }
        }
        try:
            data, metadata = self.raster.ndarray(
                inputs=["landsat:LC08:PRE:TOAR:meta_LC80270312016188_v1"],
                bands=["red"],
                resolution=960,
                cutline=json.dumps(shape),
            )
            self.assertEqual(data.shape, (245, 238))
            self.assertEqual(data.dtype, np.uint16)
            self.assertEqual(len(metadata["bands"]), 1)
        except ImportError:
            pass

    def test_thumbnail(self):
        r = self.raster.raster(
            inputs=["landsat:LC08:PRE:TOAR:meta_LC80270312016188_v1"],
            bands=["red", "green", "blue", "alpha"],
            dimensions=[256, 256],
            scales=[[0, 4000]] * 4,
            output_format="PNG",
            data_type="Byte",
        )
        self.assertTrue("metadata" in r)
        self.assertTrue("files" in r)
        self.assertIsNotNone(
            r["files"][
                "landsat:LC08:PRE:TOAR:meta_LC80270312016188_v1_red-green-blue-alpha.png"
            ]
        )

    def test_iter_dltiles_from_place(self):
        n = 0
        for tile in self.raster.iter_dltiles_from_shape(
            30.0, 2048, 16, iowa_geom, maxtiles=4
        ):
            n += 1
        self.assertEqual(n, 58)

    def test_dltiles_from_place(self):
        dltiles_feature_collection = self.raster.dltiles_from_shape(
            30.0, 2048, 16, iowa_geom
        )
        self.assertEqual(len(dltiles_feature_collection["features"]), 58)

    def test_dltiles_from_latlon(self):
        dltile_feature = self.raster.dltile_from_latlon(45.0, -90.0, 30.0, 2048, 16)
        self.assertEqual(dltile_feature["properties"]["key"], "2048:16:30.0:16:-4:81")

    def test_dltile(self):
        with self.assertRaises(ValueError):
            self.raster.dltile(None)
        with self.assertRaises(ValueError):
            self.raster.dltile("")
        dltile_feature = self.raster.dltile("2048:16:30.0:16:-4:81")
        self.assertEqual(dltile_feature["properties"]["key"], "2048:16:30.0:16:-4:81")

    def test_raster_dltile(self):
        dltile_feature = self.raster.dltile_from_latlon(41.0, -94.0, 30.0, 256, 16)
        arr, meta = self.raster.ndarray(
            inputs=["landsat:LC08:PRE:TOAR:meta_LC80270312016188_v1"],
            bands=["red", "green", "blue", "alpha"],
            dltile=dltile_feature["properties"]["key"],
        )
        self.assertEqual(arr.shape[0], 256 + 2 * 16)
        self.assertEqual(arr.shape[1], 256 + 2 * 16)
        self.assertEqual(arr.shape[2], 4)

    def test_raster_dltile_dict(self):
        dltile_feature = self.raster.dltile_from_latlon(41.0, -94.0, 30.0, 256, 16)
        arr, meta = self.raster.ndarray(
            inputs=["landsat:LC08:PRE:TOAR:meta_LC80270312016188_v1"],
            bands=["red", "green", "blue", "alpha"],
            dltile=dltile_feature,
        )
        self.assertEqual(arr.shape[0], 256 + 2 * 16)
        self.assertEqual(arr.shape[1], 256 + 2 * 16)
        self.assertEqual(arr.shape[2], 4)


if __name__ == "__main__":
    unittest.main()

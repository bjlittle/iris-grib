# Copyright iris-grib contributors
#
# This file is part of iris-grib and is released under the BSD license.
# See LICENSE in the root of the repository for full licensing details.
"""
Integration tests to confirm data is loaded correctly.

"""

# import iris_grib.tests first so that some things can be initialised
# before importing anything else.
import iris_grib.tests as tests

import numpy as np
import numpy.ma as ma

from iris import load_cube


class TestImport(tests.IrisGribTest):
    def test_gdt1(self):
        path = tests.get_data_path(("GRIB", "rotated_nae_t", "sensible_pole.grib2"))
        cube = load_cube(path)
        self.assertCMLApproxData(cube)

    def test_gdt90_with_bitmap(self):
        path = tests.get_data_path(("GRIB", "umukv", "ukv_chan9.grib2"))
        cube = load_cube(path)
        # Pay particular attention to the orientation.
        self.assertIsNot(cube.data[0, 0], ma.masked)
        self.assertIs(cube.data[-1, 0], ma.masked)
        self.assertIs(cube.data[0, -1], ma.masked)
        self.assertIs(cube.data[-1, -1], ma.masked)
        x = cube.coord("projection_x_coordinate").points
        y = cube.coord("projection_y_coordinate").points
        self.assertGreater(x[0], x[-1])  # Decreasing X coordinate
        self.assertLess(y[0], y[-1])  # Increasing Y coordinate
        # Check everything else.
        self.assertCMLApproxData(cube)


class TestGDT30(tests.IrisGribTest):
    def test_lambert(self):
        path = tests.get_data_path(("GRIB", "lambert", "lambert.grib2"))
        cube = load_cube(path)
        self.assertCMLApproxData(cube)


class TestGDT40(tests.IrisGribTest):
    def test_regular(self):
        path = tests.get_data_path(("GRIB", "gaussian", "regular_gg.grib2"))
        cube = load_cube(path)
        self.assertCMLApproxData(cube)

    def test_reduced(self):
        path = tests.get_data_path(("GRIB", "reduced", "reduced_gg.grib2"))
        cube = load_cube(path)
        self.assertCMLApproxData(cube)


class TestDRT3(tests.IrisGribTest):
    def test_grid_complex_spatial_differencing(self):
        path = tests.get_data_path(("GRIB", "missing_values", "missing_values.grib2"))
        cube = load_cube(path)
        self.assertCMLApproxData(cube)


class TestDataProxy(tests.IrisGribTest):
    def test_data_representation__no_bitsPerValue(self):
        """Ensures that zero data is auto-generated."""
        # This test file contains one GRIB2 message with no data payload
        # in Data Section [7], but has "bitsPerValue=0" in the Data
        # Representation Section [5] to trigger auto-generation of zero
        # data payload by the DataProxy.
        path = tests.get_data_path(
            ("GRIB", "missing_values", "ice_severity__no_bitsPerValue.grib2")
        )
        cube = load_cube(path)
        self.assertCML(cube)
        self.assertEqual(0, np.sum(cube.data))


if __name__ == "__main__":
    tests.main()

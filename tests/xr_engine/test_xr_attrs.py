#!/usr/bin/env python3

# (C) Copyright 2020 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

import os
import sys

import pytest

from earthkit.data import from_source
from earthkit.data.testing import earthkit_remote_test_data_file

here = os.path.dirname(__file__)
sys.path.insert(0, here)
from xr_engine_fixtures import compare_coords  # noqa: E402
from xr_engine_fixtures import compare_dims  # noqa: E402


@pytest.mark.cache
@pytest.mark.parametrize(
    "kwargs,coords,dims,attrs",
    [
        (
            {
                "dims_as_attrs": None,
                "time_dim_mode": "raw",
                "decode_times": False,
                "decode_timedelta": False,
            },
            {
                "date": [20240603, 20240604],
                "time": [0, 1200],
                "step": [0, 6],
                "levelist": [500, 700],
            },
            {"date": 2, "time": 2, "step": 2, "levelist": 2},
            {},
        ),
        (
            {
                "dims_as_attrs": "levtype",
                "time_dim_mode": "raw",
                "decode_times": False,
                "decode_timedelta": False,
            },
            {
                "date": [20240603, 20240604],
                "time": [0, 1200],
                "step": [0, 6],
                "levelist": [500, 700],
            },
            {"date": 2, "time": 2, "step": 2, "levelist": 2},
            {"levtype": 2},
        ),
    ],
)
def test_xr_dims_as_attrs(kwargs, coords, dims, attrs):
    ds0 = from_source(
        "url", earthkit_remote_test_data_file("test-data", "xr_engine", "level", "pl_small.grib")
    )

    ds = ds0.to_xarray(**kwargs)
    compare_coords(ds, coords)
    compare_dims(ds, dims, sizes=True)

    for k, v in attrs.items():
        ds["t"].attrs[k] == v

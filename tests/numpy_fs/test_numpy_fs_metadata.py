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

import numpy as np
import pytest

here = os.path.dirname(__file__)
sys.path.insert(0, here)
from numpy_fs_fixtures import load_numpy_fs, load_numpy_fs_file  # noqa: E402

# Note: Almost all grib metadata tests are also run for numpyfs.
# See grib/test_grib_metadata.py


def test_numpy_fs_grib_values_metadata():
    ds, _ = load_numpy_fs(1)

    # values metadata
    keys = [
        "min",
        "max",
        "avg",
        "ds",
        "skew",
        "kurt",
        "isConstant",
        "const",
        "bitmapPresent",
        "numberOfMissing",
    ]
    for k in keys:
        assert ds[0].metadata(k, default=None) is None, k
        with pytest.raises(KeyError):
            ds[0].metadata(k)


def test_numpy_fs_grib_values_metadata_internal():
    ds, _ = load_numpy_fs(1)

    keys = {
        "shortName": "2t",
        "grib.shortName": "2t",
    }

    for k, v in keys.items():
        assert ds[0].metadata(k) == v, k

    keys = {
        "grib.min": 262.7802734375,
        "grib.max": 315.4599609375,
    }

    for k, v in keys.items():
        assert np.isclose(ds[0].metadata(k), v), k


def test_numpy_fs_metadata_namespace():
    f, _ = load_numpy_fs_file("tuv_pl.grib")

    r = f[0].metadata(namespace="vertical")
    ref = {"level": 1000, "typeOfLevel": "isobaricInhPa"}
    assert r == ref

    r = f[0].metadata(namespace=["vertical", "time"])
    ref = {
        "vertical": {"typeOfLevel": "isobaricInhPa", "level": 1000},
        "time": {
            "dataDate": 20180801,
            "dataTime": 1200,
            "stepUnits": 1,
            "stepType": "instant",
            "stepRange": "0",
            "startStep": 0,
            "endStep": 0,
            "validityDate": 20180801,
            "validityTime": 1200,
        },
    }
    assert r == ref

    r = f[0].metadata(namespace=None)
    assert isinstance(r, dict)
    assert len(r) == 177
    assert r["level"] == 1000
    assert r["stepType"] == "instant"

    r = f[0].metadata(namespace=[None])
    assert isinstance(r, dict)
    assert len(r) == 177
    assert r["level"] == 1000
    assert r["stepType"] == "instant"

    r = f[0].metadata(namespace="")
    assert isinstance(r, dict)
    assert len(r) == 177
    assert r["level"] == 1000
    assert r["stepType"] == "instant"

    r = f[0].metadata(namespace=[""])
    assert isinstance(r, dict)
    assert len(r) == 177
    assert r["level"] == 1000
    assert r["stepType"] == "instant"

    ref = {
        "geography",
        "vertical",
        "time",
        "parameter",
        "mars",
        "ls",
        "default",
    }
    r = f[0].metadata(namespace=all)
    assert isinstance(r, dict)
    assert set(r.keys()) == ref

    r = f[0].metadata(namespace=[all])
    assert isinstance(r, dict)
    assert set(r.keys()) == ref

    with pytest.raises(ValueError) as excinfo:
        r = f[0].metadata("level", namespace=["vertical", "time"])
    assert "must be a str when key specified" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        r = f[0].metadata("level", namespace=["vertical", "time"])
    assert "must be a str when key specified" in str(excinfo.value)


if __name__ == "__main__":
    from earthkit.data.testing import main

    main(__file__)

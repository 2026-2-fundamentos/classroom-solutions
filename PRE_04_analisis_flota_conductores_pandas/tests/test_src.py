"""Autograding script."""

import os


def test_01():
    """Test word count job."""

    assert os.path.exists(
        "PRE_04_analisis_flota_conductores_pandas/data/output/summary.csv"
    )
    assert os.path.exists(
        "PRE_04_analisis_flota_conductores_pandas/data/plots/top10_drivers.png"
    )

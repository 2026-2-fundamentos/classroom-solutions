"""Autograding script."""

import os


def test_01():
    """Test word count job."""

    assert os.path.exists(
        "PRE_05_analisis_flota_conductores_chatgpt/data/output/summary.csv"
    )
    assert os.path.exists(
        "PRE_05_analisis_flota_conductores_chatgpt/data/plots/top10_drivers.png"
    )

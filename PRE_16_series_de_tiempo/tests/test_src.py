import os


def test_src():

    assert os.path.exists("PRE_16_series_de_tiempo/data/output/metrics.csv")
    assert os.path.exists("PRE_16_series_de_tiempo/data/output/forecasts.csv")

import os

FOLDER = "PRE_02_airline_revenue_management"
OUTPUT_FOLDER = f"{FOLDER}/submission"


def test_01():

    assert os.path.exists(f"{OUTPUT_FOLDER}/capacity_value.csv")
    assert os.path.exists(f"{OUTPUT_FOLDER}/booking_decisions.csv")
    assert os.path.exists(f"{OUTPUT_FOLDER}/scenario_results.csv")
    assert os.path.exists(f"{OUTPUT_FOLDER}/revenue_management_cockpit.png")

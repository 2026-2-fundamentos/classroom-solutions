import os

FOLDER = "PRE_03_covid_hospital_capacity"
OUTPUT_FOLDER = f"{FOLDER}/submission"


def test_01():

    assert os.path.exists(f"{OUTPUT_FOLDER}/evaluated_plans.csv")
    assert os.path.exists(f"{OUTPUT_FOLDER}/plan_scenario_results.csv")
    assert os.path.exists(f"{OUTPUT_FOLDER}/recommended_daily_plan.csv")
    assert os.path.exists(f"{OUTPUT_FOLDER}/hospital_capacity_planner.png")

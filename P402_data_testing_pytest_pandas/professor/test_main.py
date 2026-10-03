import importlib.util
from pathlib import Path

import pandas as pd

module_path = Path(__file__).resolve().with_name("main.py")
spec = importlib.util.spec_from_file_location("p402_professor_main", module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

validate_data = module.validate_data


def test_01_accepts_data_that_satisfies_the_contract():
    dataframe = pd.DataFrame(
        [
            {
                "factory_id": 1,
                "machine_id": 2,
                "daily_units_produced": 4500,
                "factory_date": "2026-10-01",
            }
        ]
    )

    assert validate_data(dataframe) == []


def test_02_reports_a_duplicate_business_key():
    dataframe = pd.DataFrame(
        [
            {
                "factory_id": 1,
                "machine_id": 2,
                "daily_units_produced": 4500,
                "factory_date": "2026-10-01",
            },
            {
                "factory_id": 1,
                "machine_id": 2,
                "daily_units_produced": 4600,
                "factory_date": "2026-10-01",
            },
        ]
    )

    assert validate_data(dataframe) == [
        "La llave factory_id-machine_id-factory_date debe ser única."
    ]

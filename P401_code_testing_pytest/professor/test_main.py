import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from main import build_certified_driver_totals


def test_01_aggregates_only_certified_drivers():
    drivers = pd.DataFrame(
        [
            {"driverId": 1, "name": "Ana", "certified": "Y"},
            {"driverId": 2, "name": "Bruno", "certified": "N"},
        ]
    )
    timesheet = pd.DataFrame(
        [
            {"driverId": 1, "hours-logged": 8, "miles-logged": 240},
            {"driverId": 1, "hours-logged": 6, "miles-logged": 180},
            {"driverId": 2, "hours-logged": 9, "miles-logged": 270},
        ]
    )

    summary = build_certified_driver_totals(drivers, timesheet)

    assert summary.to_dict("records") == [
        {"driverId": 1, "name": "Ana", "total_hours": 14, "total_miles": 420}
    ]

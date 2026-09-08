"""Autograding script"""

import json
import os


def test_01():
    """Test app"""

    assert os.path.exists("files/drivers.json")

    # read the json file "drivers.json"
    with open("files/drivers.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 34

    assert data[0] == {
        "driverId": "10",
        "name": "George Vetticaden",
        "ssn": "621011971",
        "location": "244-4532 Nulla Rd.",
        "certified": "N",
        "wage-plan": "miles",
    }

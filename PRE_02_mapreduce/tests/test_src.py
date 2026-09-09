import os

from ..src.word_count_2 import *

FOLDER = "PRE_02_mapreduce"


def test_01():

    initialize_folder(f"{FOLDER}/data/input/")
    delete_folder(f"{FOLDER}/data/output/")
    generate_file_copies(1000)

    hadoop(
        input_folder=f"{FOLDER}/data/input/",
        output_folder=f"{FOLDER}/data/output/",
        mapper_fn=mapper,
        reducer_fn=reducer,
    )

    if not os.path.exists(f"{FOLDER}/data/output/"):
        raise Exception("Output directory does not exist")

    if not os.path.exists(f"{FOLDER}/data/output/_SUCCESS"):
        raise Exception("Output directory is empty")

    with open(f"{FOLDER}/data/output/part-00000", "r", encoding="utf-8") as f:
        lines = f.readlines()
        result = {}
        for line in lines:
            key, value = line.strip().split("\t")
            result[key] = int(value)

    assert result["analytics"] == 5000
    assert result["business"] == 7000
    assert result["by"] == 3000
    assert result["algorithms"] == 2000
    assert result["analysis"] == 4000

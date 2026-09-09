import os

from ..src.word_count_2 import *


def test_01():

    initialize_folder("PRE_02_mapreduce/data/input/")
    delete_folder("PRE_02_mapreduce/data/output/")
    generate_file_copies(1000)

    hadoop(
        input_folder="PRE_02_mapreduce/data/input/",
        output_folder="PRE_02_mapreduce/data/output/",
        mapper_fn=mapper,
        reducer_fn=reducer,
    )

    if not os.path.exists("PRE_02_mapreduce/data/output/"):
        raise Exception("Output directory does not exist")

    if not os.path.exists("PRE_02_mapreduce/data/output/_SUCCESS"):
        raise Exception("Output directory is empty")

    with open("PRE_02_mapreduce/data/output/part-00000", "r", encoding="utf-8") as f:
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

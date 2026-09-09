import os

FOLDER = "PRE_13_clustering_demanda/data/output"


def test_homework():
    """Test the homework."""

    assert os.path.exists(f"{FOLDER}/demanda-comercial-patrones-ejemplo.png")
    assert os.path.exists(f"{FOLDER}//demanda-comercial-perfiles.png")
    assert os.path.exists(f"{FOLDER}//demanda-comercial.png")

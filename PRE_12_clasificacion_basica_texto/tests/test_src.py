import pickle

import pandas as pd
from sklearn.metrics import accuracy_score


def test_01():

    dataframe = pd.read_csv(
        "PRE_12_clasificacion_basica_texto/data/input/sentences.csv.zip",
        index_col=False,
        compression="zip",
    )

    with open("PRE_12_clasificacion_basica_texto/data/output/clf.pkl", "rb") as file:
        clf = pickle.load(file)

    with open(
        "PRE_12_clasificacion_basica_texto/data/output/vectorizer.pkl", "rb"
    ) as file:
        vectorizer = pickle.load(file)

    accuracy = accuracy_score(
        y_true=dataframe.target,
        y_pred=clf.predict(vectorizer.transform(dataframe.phrase)),
    )

    assert accuracy > 0.854

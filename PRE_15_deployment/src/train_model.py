import os
import pickle

import pandas as pd  # type: ignore
from sklearn.linear_model import LinearRegression  # type: ignore

df = pd.read_csv("PRE_15_deployment/data/input/house_data.csv")

features = df[
    [
        "bedrooms",
        "bathrooms",
        "sqft_living",
        "sqft_lot",
        "floors",
        "waterfront",
        "condition",
    ]
]

target = df[["price"]]

estimator = LinearRegression()
estimator.fit(features, target)

if not os.path.exists("PRE_15_deployment/data/output"):
    os.makedirs("PRE_15_deployment/data/output")

with open("PRE_15_deployment/data/output/house_predictor.pkl", "wb") as file:
    pickle.dump(estimator, file)

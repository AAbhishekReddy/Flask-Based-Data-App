import numpy as np
import pandas as pd
import os
import joblib

def nyse_reg(nyse_data):
    file_path = os.path.dirname(os.path.realpath(__file__))

    nyse_dataframe = {"symbol": nyse_data[0],
            "open": nyse_data[1],
            "high": nyse_data[2],
            "low": nyse_data[3]}
    nyse_dataframe = pd.DataFrame(nyse_dataframe, index = [0])

    if nyse_data[0] == "AMZN":
        file_path = os.path.join(file_path, "amazon_regression.sav")
    elif nyse_data[0] == "MSFT":
        file_path = os.path.join(file_path, "microsoft_regression.sav")
    else:
        file_path = os.path.join(file_path, "apple_regression.sav")
    
    reg = joblib.load(file_path)

    arr = np.array([nyse_data[1], nyse_data[2], nyse_data[3]])
    arr = arr.astype("float64")

    prediction = reg.predict(arr.reshape(1,-1))

    return prediction, nyse_dataframe
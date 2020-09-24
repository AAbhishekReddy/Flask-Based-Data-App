import numpy as np
import os
import joblib

def nyse_reg(nyse_data):
    file_path = os.path.dirname(os.path.realpath(__file__))

    if nyse_data[0] == "AMZN":
        file_path = os.path.join(file_path, "amazon_regression.sav")
    elif nyse_data[0] == "MSFT":
        file_path = os.path.join(file_path, "microsoft_regression.sav")
    else:
        file_path = os.path.join(file_path, "apple_regression.sav")
    
    reg = joblib.load(file_path)
    arr = np.array([nyse_data[1], nyse_data[2], nyse_data[3]])
    arr = arr.astype("float64")

    nyse_data.append(reg.predict(arr.reshape(1,-1))[0])

    return nyse_data

def beer_reg(beer_data):
    arr = np.array([beer_data[1], beer_data[2], beer_data[3]])
    file_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(file_path, "beer_regression.sav")
    beer_lr = joblib.load(file_path)
    beer_data.append(beer_lr.predict(arr.reshape(1,-1))[0])
    return beer_data
import numpy as np
import os
import joblib
import pickle

def nyse_reg(nyse_data):
    file_path = os.path.dirname(os.path.realpath(__file__))

    # if nyse_data[0] == "AMZN":
    #     file_path = os.path.join(file_path, "amazon_regression.sav")
    # elif nyse_data[0] == "MSFT":
    #     file_path = os.path.join(file_path, "microsoft_regression.sav")
    # else:
    #     file_path = os.path.join(file_path, "apple_regression.sav")

    if nyse_data[0] == "AMZN":
        file_path = os.path.join(file_path, "amazon_pickle.h5")
    elif nyse_data[0] == "MSFT":
        file_path = os.path.join(file_path, "microsoft_pickle.h5")
    else:
        file_path = os.path.join(file_path, "aapl_pickle.h5")
    
    # reg = joblib.load(file_path)
    reg = pickle.load(open(file_path, 'rb')) 
    arr = np.array([nyse_data[1], nyse_data[2], nyse_data[3]])
    arr = arr.astype("float64")

    nyse_data.append(reg.predict(arr.reshape(1,-1))[0])
    print(nyse_data)

    return nyse_data

def beer_reg(beer_data):
    arr = np.array([beer_data[1], beer_data[2], beer_data[3]])
    file_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(file_path, "beer_pickle.h5")
    # file_path = os.path.join(file_path, "beer_regression.sav")
    # beer_lr = joblib.load(file_path)

    beer_pickle = pickle.load(open(file_path, 'rb')) 

    # beer_data.append(beer_lr.predict(arr.reshape(1,-1))[0])
    beer_data.append(beer_pickle.predict(arr.reshape(1,-1))[0])
    
    return beer_data
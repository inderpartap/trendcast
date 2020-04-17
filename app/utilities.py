import json
import pickle

import numpy as np
import pandas as pd
import requests
from fbprophet import Prophet
from fbprophet.plot import add_changepoints_to_plot
from fbprophet.plot import plot_yearly

from utils.utils import *
from utils.department_modeling import Department_Modeling

# facebook prophet


# serializing json data for compatibility with frontend
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        return json.JSONEncoder.default(self, obj)

# load and return data only for that city
def load_data(city):
    city = str.lower(city)
    df = pd.read_csv("../data/end_dates.csv")
    df = df[df.city == city]
    return df

# to show timeseries for the given city
def static_data(cityname):
    city = str.lower(cityname)
    df = pd.read_csv("../data/trendcast_dataset.csv")
    df = df[df.city == city]
    df = df.sort_values("date")
    df = df[["date", "city", "totalQuantity", "totalSales"]]
    ser = json.dumps(df, cls=JSONEncoder)
    unser = json.loads(ser)
    return unser

# get the weather data for the dates provided
def get_weather(dates, cityname):
    df = pd.read_csv("../data/city_id_names.csv")
    df = df[df["name"] == str.lower(cityname)]
    city_id = df["station_id"].iat[-1]

    str_date = dates["ds"].apply(lambda x: x.strftime("%Y-%m-%d"))	# convert datetime to string
    start_date = str_date.head(1)
    end_date = str_date.tail(1)

    response = send_request(
        api="weather",
        end_point="daily",
        params=dict(station=int(city_id), start=start_date, end=end_date),
    )
    response_df = pd.DataFrame(response)
    weather_df = pd.merge(pd.DataFrame(str_date), response_df, left_on='ds', right_on='date', how = 'left') # join based on the dates
    weather_df = weather_df[['ds', 'temperature']]
    weather_df['temperature'] = weather_df['temperature'].interpolate(method='nearest', axis=0).ffill().bfill() # fill in missing values
    return weather_df

def get_predictions(cityname, path_without_weather, path_with_weather, cityflag=None):
    df = load_data(cityname)
    df["y"] = 0
    temp = df[["ds", "y"]] # get the last 2 dates of the city records

    m = Prophet()
    m.fit(temp)

    dates = m.make_future_dataframe(periods=7)
    dates = dates.drop([0, 1]).reset_index(drop=True)   # get the next 7 dates

    data = get_weather(dates, cityname) # get weather information

    # get predictions without weather
    dates_only = pd.DataFrame(data["ds"])
    if cityflag:
        wo_weather_model = Prophet()
        wo_weather_model = pickle.load(open(path_without_weather, "rb"))
        predictions_base = wo_weather_model.predict(dates_only)

        output = predictions_base[["ds", "yhat"]]
        output["yhat"] = np.exp(output["yhat"])
        output["ds"] = output["ds"].apply(lambda x: x.strftime("%Y.%m.%d"))
        ser = json.dumps(output, cls=JSONEncoder)
        unser_base = json.loads(ser)

        # get predictions with weather
        w_weather_model = Prophet()
        w_weather_model = pickle.load(open(path_with_weather, "rb"))
        predictions_weather = w_weather_model.predict(data)

        output = predictions_weather[["ds", "yhat"]]
        output["ds"] = output["ds"].apply(lambda x: x.strftime("%Y.%m.%d"))
        output["yhat"] = np.exp(output["yhat"])
        ser = json.dumps(output, cls=JSONEncoder)
        unser_weather = json.loads(ser)
    else:
        wo_weather_model = Department_Modeling()
        wo_weather_model = pickle.load(open(path_without_weather, "rb"))
        predictions_base = wo_weather_model.model.predict(dates_only)

        output = predictions_base[["ds", "yhat"]]
        output["yhat"] = np.exp(output["yhat"])
        output["ds"] = output["ds"].apply(lambda x: x.strftime("%Y.%m.%d"))
        ser = json.dumps(output, cls=JSONEncoder)
        unser_base = json.loads(ser)
        
        # get predictions with weather
        w_weather_model = Department_Modeling()
        w_weather_model = pickle.load(open(path_with_weather, "rb"))
        predictions_weather = w_weather_model.model.predict(data)

        output = predictions_weather[["ds", "yhat"]]
        output["ds"] = output["ds"].apply(lambda x: x.strftime("%Y.%m.%d"))
        output["yhat"] = np.exp(output["yhat"])
        ser = json.dumps(output, cls=JSONEncoder)
        unser_weather = json.loads(ser)


    return unser_base, unser_weather

# get city level model predictions
def citylevel(cityname):
	# generate pathnames for models
    city_file = str.lower(cityname.replace(" ", "_"))
    path_without_weather = "../models/sales/without_weather/" + city_file + ".pkl"
    path_with_weather = "../models/sales/weather/" + city_file + ".pkl"

    base_pred, weather_pred = get_predictions(cityname, path_without_weather, path_with_weather, cityflag = 1)

    return base_pred, weather_pred

# get department level model predictions
def deptlevel(cityname, department):
    # generate pathnames for models
    city_file = str.lower(cityname.replace(" ", "_"))
    path_without_weather = ("../models/department_level/without_weather/" +
                            city_file + "_" + department + "_model.pkl")
    path_with_weather = ("../models/department_level/weather/" + city_file +
                         "_" + department + "_model.pckl")

    base_pred, weather_pred = get_predictions(cityname, path_without_weather, path_with_weather)

    return base_pred, weather_pred

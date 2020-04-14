import json
import pickle

import numpy as np
import pandas as pd
import requests
from fbprophet import Prophet
from fbprophet.plot import add_changepoints_to_plot
from fbprophet.plot import plot_yearly

from utils.utils import *

# facebook prophet


# serializing json data for compatibility with frontend
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        return json.JSONEncoder.default(self, obj)


def load_data(city):
    city = str.lower(city)
    df = pd.read_csv("../data/trendcast_dataset.csv")
    df = df[df.city == city]
    df = df.sort_values("date")
    return df


def static_data(cityname):
    df = load_data(cityname)
    df = df[["date", "city", "totalQuantity", "totalSales"]]
    ser = json.dumps(df, cls=JSONEncoder)
    unser = json.loads(ser)
    return unser


def get_weather(dates, cityname):
    df = pd.read_csv("../data/city_id_names.csv")
    df = df[df["name"] == str.lower(cityname)]
    city_id = df["station_id"].iat[-1]

    str_date = dates["ds"].apply(lambda x: x.strftime("%Y.%m.%d"))
    start_date = str_date.head(1)
    end_date = str_date.tail(1)

    response = send_request(
        api="weather",
        end_point="daily",
        params=dict(station=int(city_id), start=start_date, end=end_date),
    )
    response_df = pd.DataFrame(response)
    dates["temperature"] = response_df[["temperature_min",
                                        "temperature_max"]].mean(axis=1)
    return dates


def citylevel(cityname):
    city_file = str.lower(cityname.replace(" ", "_"))
    path_without_weather = "../models/sales/without_weather/" + city_file + ".pkl"
    path_with_weather = "../models/sales/weather/" + city_file + ".pkl"

    df = load_data(cityname)
    df["y"] = 0
    df = df.rename(columns={"date": "ds"})
    temp = df[["ds", "y"]].tail(2)

    m = Prophet()
    m.fit(temp)

    dates = m.make_future_dataframe(periods=7)
    dates = dates.drop([0, 1]).reset_index(drop=True)

    data = get_weather(dates, cityname)

    dates_only = pd.DataFrame(data["ds"])
    wo_weather_model = Prophet()
    wo_weather_model = pickle.load(open(path_without_weather, "rb"))
    predictions_base = wo_weather_model.predict(dates_only)

    output = predictions_base[["ds", "yhat"]]
    output["yhat"] = np.exp(output["yhat"])
    output["ds"] = output["ds"].apply(lambda x: x.strftime("%Y.%m.%d"))
    ser = json.dumps(output, cls=JSONEncoder)
    unser_base = json.loads(ser)

    w_weather_model = Prophet()
    w_weather_model = pickle.load(open(path_with_weather, "rb"))
    predictions_weather = w_weather_model.predict(data)

    output = predictions_weather[["ds", "yhat"]]
    output["ds"] = output["ds"].apply(lambda x: x.strftime("%Y.%m.%d"))
    output["yhat"] = np.exp(output["yhat"])
    ser = json.dumps(output, cls=JSONEncoder)
    unser_weather = json.loads(ser)

    return unser_base, unser_weather


def deptlevel(cityname, department):
    df = load_data(cityname)

    city_file = str.lower(cityname)
    path_without_weather = ("../models/department_level/without_weather/" +
                            cityname + "_" + department + "_model.pkl")
    path_with_weather = ("../models/department_level/weather/" + cityname +
                         "_" + department + "_model.pkl")

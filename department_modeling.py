import os
import pickle
import zipfile
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from fbprophet import Prophet
from sklearn.metrics import mean_squared_error
from statistics import mean
import data_to_timeseriesData as data_to_ts
from utils.utils import *


class Department_Modeling:
    def __init__(self):
        """
        Instantiate the prophet model

        """
        # holidays and special days
        playoffs = pd.DataFrame({
            "holiday":
            "playoff",
            "ds":
            pd.to_datetime([
                "2014-11-13",
                "2015-11-12",
                "2016-11-10",
                "2017-11-16",
                "2018-11-15",
                "2019-11-14",
                "2014-12-26",
                "2015-11-27",
                "2016-12-26",
            ]),
            "lower_window":
            0,
            "upper_window":
            0,
        })
        # additional effect on top of the playoffs
        # black friday each year
        superbowls = pd.DataFrame({
            "holiday":
            "superbowl",
            "ds":
            pd.to_datetime([
                "2014-11-13",
                "2015-11-12",
                "2016-11-10",
                "2017-11-16",
                "2018-11-15",
                "2019-11-14",
            ]),
            "lower_window":
            0,
            "upper_window":
            0,
        })
        holidays = pd.concat((playoffs, superbowls))
        self.model = Prophet(daily_seasonality=True, holidays=holidays)
        self.model.add_country_holidays(country_name="CA")  # Canada holidays

    def fit_model(self, df, y, regressors):
        """
            give a list of regressors present in the dataframe that needed to be addeed to make the model
            y should be the target or the response variable

        """

        for reg in regressors:
            self.model.add_regressor(reg)

        # make copy of dataframe and transform it
        df_copy = df.copy()
        df_copy = df_copy.reset_index()
        df_copy = df_copy.rename({"date": "ds", y: "y"}, axis=1)

        self.fit_model = self.model.fit(df_copy)
        return self

    def predict_model_val(self, X, y):
        """
            Predict output for a dataframe X

        """
        X_copy = X.copy()
        X_copy = X_copy.reset_index()
        X_copy = X_copy.rename({"date": "ds", y: "y"}, axis=1)
        self.forecast_vals = self.fit_model.predict(X_copy)
        return self

    def evaluate_model(self, X_orig, y_orig):
        """
        Evaluate model performance
        """

        X_orig = X_orig.reset_index().drop(columns=["date"])
        print(self.forecast_vals["yhat"])
        np.nan_to_num(self.forecast_vals['yhat'],
                      posinf=np.inf, neginf=-np.inf)
        rmse = mean_squared_error(
            y_true=X_orig[y_orig], y_pred=self.forecast_vals['yhat'])
        mae = abs(self.forecast_vals["yhat"] - X_orig[y_orig]).mean()
        return (mae, rmse)


def saving_model(model, filename, isWeather):
    print("saving model")
    if isWeather:
        filesavingpath = (modelpath["department_models"] + "/weather/" +
                          filename + ".pckl")
    else:
        filesavingpath = (modelpath["department_models"] +
                          "/without_weather/" + filename + ".pckl")

    with open(filesavingpath, "wb") as fout:
        pickle.dump(model, fout)

    return


# for each city, take one department. measure some threshold. After that model it and save it
def make_city_dept_models(cities_list, department_list, df, isWeather):
    # split into train and test

    no_months = 3
    startdate = min(df.date).strftime('%Y-%m-%d')
    endDate = max(df.date).strftime('%Y-%m-%d')
    X_train, X_test = data_to_ts.split_train_test_ts(
        df, startdate, endDate, no_months)
    avg_loss = []

    for city in cities_list:
        for dept in department_list:
            filtered_train_df = X_train[(X_train["city"] == city) & (
                X_train["department"] == dept)]
            filtered_test_df = X_test[(X_test["city"] == city) & (
                X_test["department"] == dept)]
            # define a threshold
            if len(filtered_train_df) >= 1000:
                if isWeather:
                    columns_to_drop = [
                        "province",
                        "city",
                        "department",
                        "peakgust",
                        "pressure",
                        "temperature_min",
                        "temperature_max",
                        "winddirection",
                    ]
                    regressors = ["temperature"]
                else:
                    columns_to_drop = [
                        "province",
                        "city",
                        "department",
                        "peakgust",
                        "pressure",
                        "temperature_min",
                        "temperature_max",
                        "winddirection",
                        "windspeed",
                        "precipitation",
                        "temperature",
                    ]
                    regressors = []
                filtered_train_df = filtered_train_df.drop(
                    columns=columns_to_drop)
                filtered_test_df = filtered_test_df.drop(
                    columns=columns_to_drop)

                model_obj = Department_Modeling()
                fit_model = model_obj.fit_model(filtered_train_df, "totalQuantity",
                                                regressors)
                pred_vals = fit_model.predict_model_val(
                    filtered_test_df, "totalQuantity")
                (mae, rmse) = pred_vals.evaluate_model(
                    filtered_test_df, "totalQuantity")
                print("MAE for City {} and Dept {} is {}".format(
                    city, dept, mae))
                print("RMSE for City {} and Dept {} is {}".format(
                    city, dept, rmse))
                # save model
                avg_loss.append(rmse)
                saving_model(model_obj, city + "_" + dept + "_model",
                             isWeather)

    if(isWeather):
        text = "with weather"
    else:
        text = "without weather"
    print("Average Loss across all cities and departments for model {} is {}".format(
        text, mean(avg_loss.mean)))


def main():
    department_df = pd.read_csv(
        datapath["department_level_data"],
        parse_dates=["date"],
        date_parser=pd.to_datetime,
    )

    # get cities
    cities_list = department_df["city"].unique()
    # get department list
    department_list = department_df["department"].unique()

    make_city_dept_models(cities_list,
                          department_list,
                          department_df,
                          isWeather=False)


if __name__ == "__main__":
    main()

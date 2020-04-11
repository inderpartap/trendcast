import pandas as pd
from datetime import datetime
import numpy as np
from utils.utils import *
import zipfile
import os
from fbprophet import Prophet
import matplotlib.pyplot as plt
import pickle
import data_to_timeseriesData as data_to_ts


class Department_Modeling:
    def __init__(self):
        """
        Instantiate the prophet model

        """
        self.model = Prophet()

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
        mae = abs(self.forecast_vals["yhat"] - X_orig[y_orig]).mean()
        return mae


def saving_model(model, filename, isWeather):
    print("saving model")
    if isWeather:
        filesavingpath = (
            modelpath["department_models"] + "/weather/" + filename + ".pckl"
        )
    else:
        filesavingpath = (
            modelpath["department_models"] + "/without_weather/" + filename + ".pckl"
        )

    with open(filesavingpath, "wb") as fout:
        pickle.dump(model, fout)

    return


# for each city, take one department. measure some threshold. After that model it and save it
def make_city_dept_models(cities_list, department_list, df, isWeather):
    # split into train and test

    no_months = 3

    for city in cities_list:
        for dept in department_list:
            filtered_df = df[(df["city"] == city) & (df["department"] == dept)]
            # define a threshold
            if len(filtered_df) >= 1000:
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
                    regressors = ["totalQuantity", "temperature"]
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
                    regressors = ["totalQuantity"]
                filtered_df = filtered_df.drop(columns=columns_to_drop)
                startdate = min(filtered_df.date).strftime("%Y-%m-%d")
                endDate = max(filtered_df.date).strftime("%Y-%m-%d")
                X_train, X_test = data_to_ts.split_train_test_ts(
                    filtered_df, startdate, endDate, no_months
                )

                model_obj = Department_Modeling()
                fit_model = model_obj.fit_model(X_train, "totalSales", regressors)
                pred_vals = fit_model.predict_model_val(X_test, "totalSales")
                mae = pred_vals.evaluate_model(X_test, "totalSales")
                print("MAE for City {} and Dept {} is {}".format(city, dept, mae))
                # save model
                saving_model(model_obj, city + "_" + dept + "_model", isWeather)


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

    make_city_dept_models(cities_list, department_list, department_df, isWeather=False)


if __name__ == "__main__":
    main()

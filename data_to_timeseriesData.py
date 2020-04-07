from datetime import datetime

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.model_selection import TimeSeriesSplit

from utils.utils import datapath


# make sure we have a "DateTime column in the df"
# creating date features useful in timeseries modeling
def get_date_features(df):
    if "DateTime" in df.columns:
        df["year"] = df.DateTime.dt.year
        df["month"] = df.DateTime.dt.month
        df["day"] = df.DateTime.dt.day
        df["dayOfWeek"] = df.DateTime.dt.dayofweek

    return df


# create a new column with boolean feature if weekend or not
def create_weekend_feature(df, col):
    df.loc[df[col] == 5, "isWeekend"] = 1
    df.loc[df[col] == 6, "isWeekend"] = 1
    df["isWeekend"].fillna(0, inplace=True)
    return df


# sorting index by date, splitting then based on dates


def split_train_test_ts(df, startdate, endDate, no_months):

    # sorting the index to split the data based on dates
    df = df.sort_index()

    # creating datetime obj
    datetime_obj = datetime.strptime(endDate, "%Y-%m-%d")
    new_year = datetime_obj.year
    new_month = (datetime_obj.month - no_months) % 12
    if no_months >= datetime_obj.month:
        new_year = datetime_obj.year - 1

    # getting the start date for test data
    test_data_startdate = datetime(new_year, new_month, 1).strftime("%Y-%m-%d")

    # splitting
    X_train = df.loc[startdate:test_data_startdate]
    X_test = df.loc[test_data_startdate:endDate]

    return (X_train, X_test)


def main():

    trendcast_data = pd.read_csv(datapath["trendcast"]).drop(["Unnamed: 0"], axis=1)
    # trendcast_data = pd.read_csv("trendcast_dataset.txt",sep=",").drop(["Unnamed: 0"], axis=1)

    # setting index of the dataframe to date
    df_dateindexed = trendcast_data.set_index("date")
    df_dateindexed["DateTime"] = pd.to_datetime(df_dateindexed.index, format="%Y-%m-%d")

    df_dateindexed = get_date_features(df_dateindexed)
    df_dateindexed = create_weekend_feature(df_dateindexed, "dayOfWeek")

    # define start date and end date for the train and test split, also with the size of test data based on number of columns
    no_months_test_data = 3
    startdate = min(df_dateindexed.index)
    endDate = max(df_dateindexed.index)

    X_train, X_test = split_train_test_ts(
        df_dateindexed, startdate, endDate, no_months_test_data
    )

    # saving train and test data
    X_train.to_csv(datapath["train_data"])
    X_test.to_csv(datapath["test_data"])


if __name__ == "__main__":
    main()

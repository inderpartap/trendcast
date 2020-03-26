import csv
import math

import pandas as pd

from utils.utils import *
from weather import get_period

# get weather daily for 6 months period max for a station id, by checking it's min and max date from retail data

# Fashion Retail Data
RETAIL_PATH = "fashion_retail.csv"
STATIONS_PATH = "stations.csv"
CITY_PATH = "citynames.csv"


def weather_daily(city_id_name_df, retail_df):

    # get start end data for a particular city
    # get data for a particular time frame
    station_names = city_id_name_df["name"].values
    station_ids = city_id_name_df["station_id"].values
    daily_data = []
    for index, val_id in enumerate(station_ids):
        # get start and end date for a particular station
        filtered_retail_data = retail_df[retail_df["city"].str.contains(
            station_names[index], case=False)]
        (start_date, end_date) = get_period(filtered_retail_data, "date")
        if not math.isnan(val_id):
            response = send_request(
                api="weather",
                end_point="daily",
                params=dict(station=int(val_id),
                            start=start_date,
                            end=end_date),
            )
            for resp_obj in response:
                resp_obj["station_id"] = int(val_id)
                resp_obj["station_name"] = station_names[index]
            daily_data.extend(response)

    return daily_data


def get_city_ids(city_data):
    # get station ids and corresponding names
    # get city_names
    city_names = city_data["city"].values
    cleaned_data = []
    # getting sation_id corresponding to city_name present in the the original_csv
    for city in city_names:
        response = send_request(api="weather",
                                end_point="stations",
                                params=dict(q=city))
        city_id = ""
        if len(response) > 0:
            for resp_val in response:
                # break if Canada is found
                if resp_val["country"] == "CA":
                    city_id = resp_val["id"]
                    break
        cleaned_data.append((city, city_id))
    return cleaned_data


# save file as csv, takes in values as list of tuples


def saveFileasCSV(filename, df, headers):
    try:
        with open(filename + ".csv", "w", newline="") as out:
            csv_out = csv.writer(out)
            csv_out.writerow(headers)
            for row in df:
                csv_out.writerow(row)
    except:
        print("File already exists")


def main():

    retail_data = load_data(RETAIL_PATH, "csv")
    city_data = load_data(CITY_PATH, "csv")

    # create cleaned station_ids with city names
    # uncomment to generate file
    # city_id_names = get_city_ids(city_data)
    # saveFileasCSV("city_id_names",city_id_names,["name","station_id"])

    city_id_names_df = load_data("city_id_names.csv", type="csv")
    daily_data = weather_daily(city_id_names_df, retail_data)
    # saving the weather daily data as csv
    pd.DataFrame(daily_data).to_csv("weather_daily.csv", index=False)


if __name__ == "__main__":
    main()

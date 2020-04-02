import csv
import json

import pandas as pd
import requests


# Global - API configurations
config = {"weather": "config/weather_api.json", "keys": "config/api_keys.json"}

datapath = {
    "stations": "data/stations.csv",
    "cities": "data/citynames.csv",
    "weather": "data/weather_daily.csv",
    "retail": "data/fashion_retail.csv",
    "trendcast": "data/trendcast_dataset.csv",
}


def load_data(PATH, type="csv"):
    df = pd.DataFrame()
    try:
        df = pd.read_csv(PATH, delimiter=",")
    except:
        print("Exception: Supports only csv file formats.")
    return df


def json_to_dict(PATH):
    dictionary = dict()
    try:
        with open(PATH) as json_file:
            dictionary = json.load(json_file)
    except:
        print("ERROR: could not load JSON file %s" % (PATH))
    return dictionary


# takes json object and writes to CSV file
def write_to_csv(json_data, outfile):
    try:
        fp = open(outfile, "w")
        output = csv.writer(fp)

        # write header
        output.writerow(json_data[0].keys())

        # write all rows
        for row in json_data:
            output.writerow(row.values())
    except:
        print("ERROR: could not open/write CSV")


def group(df, col):
    gr_df = df.groupby(col).first()
    gr_df.reset_index(inplace=True)
    return gr_df


def unique(df, col):
    lower = df[col].str.lower()  # avoid duplication
    items = lower.unique().tolist()
    return items


def send_request(api, end_point, params):
    json = json_to_dict(config[api])
    url = json["url"] + json[end_point]["end_point"]

    # check if all required parameters are passed
    for key, val in json[end_point]["params"].items():
        if val == True and key not in params:
            print('ERROR: "%s" is a required parameter for this request' % (key))
            return dict()

    # add auth key to parameters
    # TODO: Fetch keys from config in a round-robin fashion
    keys = json_to_dict(config["keys"])
    auth_key = keys["1"]["api_key"]
    params["key"] = auth_key

    response = requests.get(url=url, params=params).json()

    return response["data"]

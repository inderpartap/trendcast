import pandas as pd
from utils.utils import *


# Fashion Retail Data
RETAIL_PATH = "data/fashion_retail.csv"
STATIONS_PATH = "data/stations.csv"


# given time-series data and time-defining column-name,
# returns start and end dates (period)
def get_period(df, col):
	gr_df = group(df, col)
	start_date = gr_df[col].min()
	end_date = gr_df[col].max()

	return (start_date, end_date)


def fetch_stations(cities):
	# get station IDs for all cities
	stations = []
	for city in cities:
		response = send_request(api='weather', end_point='stations', params=dict(q=city))
		stations.extend(response)

	return stations


def main():
	# load retail sales data
	retail_data = load_data(RETAIL_PATH, 'csv')
	print(retail_data)

	# find start and end dates in dataset
	(start_date, end_date) = get_period(retail_data, 'date')
	print(start_date, end_date)

	# fetch all cities in the data
	cities = unique(retail_data, 'city')
	print(cities)

	# get station IDs for all cities
	stations = fetch_stations(cities)

	# store station information in CSV
	write_to_csv(stations, STATIONS_PATH)


if __name__=='__main__':
	main()

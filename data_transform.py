import pandas as pd

# Dataset Paths
RETAIL_PATH = "data/fashion_retail.csv"
WEATHER_PATH = "data/weather_daily.csv"
RETAIL_COMBINED_PATH = "data/trendcast_dataset.csv"


# given the retail data, create onehot-encoding of the dept wise quantity sold
# group by city to compress the data
def create_onehot(df):
	df = df.groupby(['date', 'province', 'city', 'department']).sum().reset_index()

	# set the initial values to 0
	df = df.assign(**{'department1' : 0,'department2' : 0,'department3' : 0,'department4' : 0,
									'department5' : 0,'department6' : 0,'department7' : 0,'department8' : 0,
									'department9' : 0,'department10': 0,'department11': 0,'department12': 0,
									'department13': 0,'department14': 0}) 

	# for each value in department column, update the one-hot columns
	for i in range(len(df)):
		dept_name = str(df['department'][i])
		df[dept_name][i] = df['totalQuantity'][i]
	    
	df = df.drop('department', axis = 1)
	df = df.groupby(['date', 'province', 'city']).sum().reset_index()

	return df

# add the weather information to the retail dataset
def add_weather(city_df, weather_df):
	provinces = city_df[['province', 'city']].drop_duplicates()

	# right join to keep the weather information
	result = pd.merge(city_df, weather_df, 
                  how = 'right', 
                  on = ['date', 'city'])

	result = pd.merge(provinces, result, on = ['city']) # fill in missing province values
	result = result.rename(columns={"province_x": "province"}).drop("province_y", axis =1)

	columnlist = list(result.columns.values.tolist())[3:19]
	result[columnlist] = result[columnlist].fillna(value=0) # fill the missing transaction records as 0; ~0.05% of data

	return result


def main():
	# load retail sales data
	retail_data = pd.read_csv(RETAIL_PATH).drop(["Unnamed: 0", "category", "class", "style", "vendor"], axis=1)
	retail_data['city'] = retail_data['city'].str.lower()

	# load weather data
	weather_data = pd.read_csv(WEATHER_PATH).rename(columns={"station_name": "city"}).drop("station_id", axis =1)

	# create onehot encoding of the department column
	city_data = create_onehot(retail_data)

	# add weather information
	combined_df = add_weather(city_data, weather_data)

	# store station information in CSV
	combined_df.to_csv(RETAIL_COMBINED_PATH)


if __name__=='__main__':
	main()

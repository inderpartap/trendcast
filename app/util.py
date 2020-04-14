import pandas as pd
import numpy as np
import json

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj,'to_dict'):
            return obj.to_dict()
        return json.JSONEncoder.default(self, obj)

def read_data(cityname):
	df = pd.read_csv("../data/trendcast_dataset.csv")
	df = df[df.city == cityname]
	df = df[['date', 'city', 'totalQuantity', 'totalSales']]
	df = df.sort_values('date')
	# json_data = df.to_json()
	ser = json.dumps(df, cls=JSONEncoder)
	unser=json.loads(ser)
	return unser
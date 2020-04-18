from datetime import datetime
import numpy as np
import pandas as pd


def get_data_type(path):
    dummy = pd.read_csv(path, nrows=30)
    dtype = dict(dummy.dtypes)
    return(dtype)


def feature_engineering(df):
    quarter_map = {1: 1, 2: 1, 3: 1, 4: 2, 5: 2,
                   6: 2, 7: 3, 8: 3, 9: 3, 10: 4, 11: 4, 12: 4}
    province_map = {'AB': 1, 'BC': 2, 'SK': 3}
    df['quarter'] = df.month.map(quarter_map)
    df['day_of_week_sin'] = np.sin(df.dayOfWeek*(2.*np.pi/7))
    df['day_of_week_cos'] = np.cos(df.dayOfWeek*(2.*np.pi/7))
    df['month_sin'] = np.sin((df.month-1)*(2.*np.pi/12))
    df['month_cos'] = np.cos((df.month-1)*(2.*np.pi/12))
    df['quarter_sin'] = np.sin((df.quarter-1)*(2.*np.pi/4))
    df['quarter_cos'] = np.cos((df.quarter-1)*(2.*np.pi/4))
    df['totQt_log'] = np.log(abs(df.totalQuantity)+0.0001)
    df['day_sin'] = np.sin((df.quarter-1)*(2.*np.pi/30))
    df['day_cos'] = np.cos((df.quarter-1)*(2.*np.pi/30))
    df['totQty_sqrt'] = np.sqrt(abs(df.totalQuantity))
    df['totalQty_inverse'] = 1/(df.totalQuantity+1.534)
    df['province_freq_encoding'] = df.province.map(
        df.province.value_counts())/len(df)
    df['province_label_encoding'] = df.province.map(province_map)
    df['city_freq_encoding'] = df.city.map(df.city.value_counts())/len(df)
    df['city_name_len'] = df.city.apply(lambda x: len(x))
    return(df)


def split_train_test_ts(df, startdate, endDate, no_months):

    # sorting the index to split the data based on dates
    df['Date'] = df.date
    df = df.set_index('date').sort_index()

    # creating datetime obj
    datetime_obj = datetime.strptime(endDate, '%Y-%m-%d')

    new_year = datetime_obj.year
    new_month = (datetime_obj.month - no_months) % 12
    if(no_months >= datetime_obj.month):
        new_year = datetime_obj.year - 1

    # getting the start date for test data
    test_data_startdate = datetime(new_year, new_month, 1).strftime('%Y-%m-%d')

    # splitting
    df = df.rename(columns={'Date': 'date'})
    X_train = df.loc[startdate:test_data_startdate, :]
    X_test = df.loc[test_data_startdate:endDate, :]

    return(X_train, X_test)


def main():
    # Add the directory of the following data!
    training_data = "train_data.csv"
    testing_data = "test_data.csv"

    output_training_data = "data/train_data_final.csv"
    output_testing_data = "data/test_data_final.csv"
    # reading data
    types = get_data_type(training_data)

    train = pd.read_csv(training_data, dtype=types)
    test = pd.read_csv(testing_data, dtype=types)
    df = pd.concat([train, test])
    df.iloc[:, 2:25] = df.iloc[:, 2:25].astype('float32')
    df.iloc[:, 25:46] = df.iloc[:, 25:46].astype('int32')

    # Adjusting the format of the data!
    #df = df.dropna(how="any")
    df["date"] = pd.to_datetime(df["date"])
    # Feature engineering!
    df = feature_engineering(df)

    # define start date and end date for the train and test split, also with the size of test data based on number of columns
    no_months_test_data = 3
    startdate = min(df.date).strftime('%Y-%m-%d')
    endDate = max(df.date).strftime('%Y-%m-%d')

    X_train, X_test = split_train_test_ts(
        df, startdate, endDate, no_months_test_data)

    # saving train and test data
    X_train.to_csv(output_training_data, index=False)  # datapath['train_data']
    X_test.to_csv(output_testing_data, index=False)  # datapath['test_data']

    #df.to_csv(output_directory, index=False)


if __name__ == "__main__":
    main()

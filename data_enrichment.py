import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def transform_date(df):
    
    temp=df['date'].str.split(" ", n = 1, expand = True)
    df['month']=temp[0]
    df['day']=temp[1]
    encode_months={'Jan':'01','Feb':'02','Mar':'03',"Apr":'04','May':'05','Jun':'06',
            'Jul':'07','Aug':'08',"Sep":'09','Oct':'10',"Nov":'11','Dec':'12'
             }
    df['month']=df.month.map(encode_months)
    df['year']=df.year.astype('str')
    df['date']= df.year+'-'+df.month+'-'+df.day
    df.drop(['year','day','month'],axis=1,inplace=True)
    return(df)

def add_events(df1,df2):
    df2['date']=pd.to_datetime(df2.date)
    df=pd.merge(df1,df2, how='left', on='date')
    return(df)
    
def IsNatHoliday(x):
    if x==0:
        return(0)
    else:
        return(1)
        
def fix_format(df):
    df=df.rename(columns={"name_x": "IsBlackFriday", "name_y": "IsCyberMonday"})
    df['IsBlackFriday']= df['IsBlackFriday'].map({'Black Friday':1,np.nan:0})
    df['IsCyberMonday']= df['IsCyberMonday'].map({'Cyber Monday':1,np.nan:0})
    df['IsNationalHoliday']=df['holiday']
    df=pd.get_dummies(df, columns=['holiday'])
    df['IsNationalHoliday']=df['IsNationalHoliday'].fillna(0)
    df['IsNationalHoliday']=df['IsNationalHoliday'].apply(IsNatHoliday)
    return(df)

def main():
    #Add the directory of the following data!
    training_data='train.csv'
    testing_data='train.csv'
    black_friday_data='blackfriday.csv'
    cyber_monday_data='cybermonday.csv'
    canada_holidays_data='CanadaHolidays.csv'
    output_directory='enriched_data.csv'
    
    # reading data
    train= pd.read_csv(training_data)
    test= pd.read_csv(testing_data)
    df= pd.concat([train,test])
    df_bf=pd.read_csv(black_friday_data,sep='\t')
    df_cm=pd.read_csv(cyber_monday_data,sep='\t')
    df_canh= pd.read_csv(canada_holidays_data)
    
    #Adjusting the format of the data!
    df=df.dropna(how='any')
    df['date']= pd.to_datetime(df['date'])
    df['week']=df["date"].dt.week
    
    #Transforms date column of the data in proper format!
    df_bf=transform_date(df_bf)
    df_cm=transform_date(df_cm)
    
    #Adding feature for events i.e blackfriday, cybermonday and national holidays!
    df=add_events(df,df_bf)
    df=add_events(df,df_cm)
    df=add_events(df,df_canh)
    
    df= fix_format(df)
    df.to_csv(output_directory,index=False)
	
if __name__=='__main__':
	main()
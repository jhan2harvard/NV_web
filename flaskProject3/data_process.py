import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import read_csv
from pandas import DataFrame
from pandas import Grouper
from matplotlib import pyplot

# df = pd.read_csv('static/data/US_map.csv')
df = pd.read_json("static/data/Zip_data+station.json")
wf = pd.read_json("static/data/Weather_data_bystation_Occuratio(list).json")

def location (zipcode):
    lat = df[zipcode]["Latitude"]
    long = df[zipcode]["Longitude"]
    return lat, long

def station_name (zipcode):
    station_name = df[zipcode]["Station_Name"]
    return station_name

# zipcode = 36310
# sn = station_name(zipcode)

def getWeatherData(zipcode):

    sn = station_name(zipcode)
    db = wf[sn]["DB_Temp"][1:-1]
    db = db.split(",")
    rh = wf[sn]["R_Hum(%)"][1:-1]
    rh = rh.split(",")
    wd = wf[sn]["WD"][1:-1]
    wd = wd.split(",")
    ws = wf[sn]["WS(m/s)"][1:-1]
    ws = ws.split(",")
    rnv = wf[sn]["RNV_hour"][1:-1]
    rnv = rnv.split(",")

    TLst = []
    RHLst = []
    WDLst = []
    WSLst = []
    RLst = []
    for i in range(0, len(db)):
        TLst.append(float(db[i]))
        RHLst.append(float(rh[i]))
        RLst.append(int(rnv[i]))
        WDLst.append(float(wd[i]))
        WSLst.append(float(ws[i]))

    dates2 = pd.date_range(start="2021-01-01 00:00:00", end="2021-12-31 23:00:00", freq="H")
    d = {'DB_Temp': TLst, "R_Hum(%)": RHLst, "WD": WDLst, "WS(m/s)": WSLst, 'RNV_hour': RLst}
    df = pd.DataFrame(index=dates2, data=d)

    MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

    series = df["DB_Temp"]
    # series = read_csv('daily-minimum-temperatures.csv', header=0, index_col=0, parse_dates=True, squeeze=True)
    groups = series.groupby(Grouper(freq='A'))
    years = DataFrame()
    for name, group in groups:
        years[name.year] = group.values
    years = years.T

    pyplot.matshow(years, interpolation=None, aspect='auto')
    pyplot.xticks([0, 31, 61, 92, 122, 153, 183, 214, 244, 275, 305, 336, 365], MONTHS)
    pyplot.show()

    return df

# MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

#
# series = df["DB_Temp"]
# # series = read_csv('daily-minimum-temperatures.csv', header=0, index_col=0, parse_dates=True, squeeze=True)
# groups = series.groupby(Grouper(freq='A'))
# years = DataFrame()
# for name, group in groups:
# 	years[name.year] = group.values
# years = years.T
#
# pyplot.matshow(years, interpolation=None, aspect='auto')
# pyplot.xticks([0,31,61,92,122,153,183,214,244,275,305,336,365],MONTHS)
# pyplot.show()
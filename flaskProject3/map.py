import folium
from folium import plugins
from IPython.display import IFrame
import pandas as pd
import json


def generateBaseMap(default_location=[37, -102], default_zoom_start=5):
    base_map = folium.Map(location=default_location, control_scale=True,
                          zoom_start=default_zoom_start, tiles="OpenStreetMap")
    return base_map

def generateBaseMap2(default_location=[37, -102], default_zoom_start=5):
    base_map = folium.Map(location=default_location, control_scale=True,
                          zoom_start=default_zoom_start, tiles="OpenStreetMap")
    return base_map

def map(lat,long,zoom):

    df = pd.read_csv('static/data/US_map.csv')
    colordict = {0: 'lightblue', 1: 'lightgreen', 2: 'orange', 3: 'red'}
    baseMap = generateBaseMap(default_location=[float(lat), float(long)])
    for i in range(0, len(df)):
        if 25 > float(df["NV%"][i]) > 0:
            color = colordict[3]
        elif 50 > float(df["NV%"][i]) > 25:
            color = colordict[2]
        elif 75 > float(df["NV%"][i]) > 50:
            #         color="#E37222" # tangerine
            color = colordict[1]
        else:
            #         color = "#2293e3"
            color = "#0A8A9F"  # teal

        html = str(df["Location"][i]) + "\n" + ':' + str(df["NV hours"][i]) + " hours"

        iframe = folium.IFrame(html=html, width=200, height=60)
        popup = folium.Popup(iframe, max_width=1000)

        folium.Circle(
            location=[df["Latitude"][i], df["Longtitude"][i]],
            radius=float(df["NV hours"][i]) * 15,
            popup=popup,
            color=False,
            fill=True,
            fill_color=color
        ).add_to(baseMap)
        # baseMap.save(outfile = 'templates/mapHTML.html')
    return baseMap._repr_html_()

def map2(lat,long,zoom):


    df = pd.read_csv('static/data/US_map.csv')
    # OpenStreetMap Stamen Toner CartoDB dark_matter Stamen Terrain
    colordict = {0: 'lightblue', 1: 'lightgreen', 2: 'orange', 3: 'red'}
    baseMap = generateBaseMap2(default_location=[float(lat), float(long)],default_zoom_start=zoom)

    for i in range(0, len(df)):
        if 25 > float(df["NV%"][i]) > 0:
            color = colordict[3]
        elif 50 > float(df["NV%"][i]) > 25:
            color = colordict[2]
        elif 75 > float(df["NV%"][i]) > 50:
            #         color="#E37222" # tangerine
            color = colordict[1]
        else:
            #         color = "#2293e3"
            color = "#0A8A9F"  # teal

        html = str(df["Location"][i]) + "\n" + ':' + str(df["NV hours"][i]) + " hours"
        iframe = folium.IFrame(html=html, width=200, height=60)
        popup = folium.Popup(iframe, max_width=1000)

        folium.Marker(
            location=[df["Latitude"][i], df["Longtitude"][i]],
            popup=popup,
            color=False,
            fill=True,
            fill_color=color
        ).add_to(baseMap)

    baseMap.save(outfile = 'templates/mapHTML.html')
    # return display(baseMap)
    return baseMap._repr_html_()

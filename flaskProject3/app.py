from flask import Flask, render_template, redirect, url_for, request, session
import folium
# from calculation import calculate_mode
import map
import data_process as dp
from folium import plugins
import pandas as pd
from datetime import datetime
import branca.colormap as cm
import json
import sys

app = Flask(__name__)
app.secret_key = "cgbc"
# app.config['SECRET_KEY'] = 'cgbc'
# @app.route('/')
# def homepage():
#     return render_template("main.html")

@app.route('/', methods=["POST","GET"])
def homepage():
    if request.method == "POST":
        zip = request.form["zip"]
        session["zip"]=zip
        return render_template("loc.html")
    else:
        return render_template("index.html", content="Testing")

@app.route('/region', methods=["POST","GET"])
def region():
    if request.method == "POST":
        loc = request.form["zipcode"]
        # lat = request.form["lat"]
        # long = request.form["long"]
        session["loc"]=loc
        # session["lat"]=lat
        # session["long"]=long
        a, b = dp.location(int(float(loc)))
        session["lat"]=a
        session["long"]=b
        redirect(url_for("loc"))
        # dp.getWeatherData(loc)
        return render_template("region.html")
    else:
        return render_template("region.html")

@app.route('/space', methods=["POST","GET"])
def space():
    return render_template("spatial.html")

# @app.route('/<usr>')
# def user(usr):
#     # loc = usr["zipcode"]
#     return f"<h1>{usr}</h1>"

# @app.route('/loc')
# def loc():
#     if "loc" in session:
#         loc = session["loc"]
#         lat = session["lat"]
#         long = session["long"]
#         return f"<h1>{loc}</h1><h2>{float(lat),float(long)}</h2>"
#     else:
#         return redirect(url_for("region"))

@app.route('/loc')
def loc():
    if "loc" in session:
        # loc = session["loc"]
        lat = session["lat"]
        long = session["long"]
        # map.map2(lat, long, 8)
        return map.map2(lat,long,8)

    else:
        return redirect(url_for("region"))

@app.route('/temp')
def temp():
    return render_template("chart.html")

@app.route('/mapFunction')
def get_ses():
    df = pd.read_csv('static/data/US_map.csv')
    colordict = {0: 'lightblue', 1: 'lightgreen', 2: 'orange', 3: 'red'}
    default_location = [37, -102]
    default_zoom_start = 5;
    base_map = folium.Map(location=default_location, control_scale=True,
                          zoom_start=default_zoom_start, tiles="OpenStreetMap")
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
        ).add_to(base_map)
        # baseMap.save(outfile = 'templates/mapHTML.html')
    base_map._repr_html_()

    return render_template("loc.html")

@app.route('/map')
def index():
    return map.map(37,-102,5)

@app.route('/out')
def logout():
    session.pop("loc",None)
    session.pop("lat",None)
    session.pop("long",None)


if __name__ == '__main__':
    app.run(debug=True)

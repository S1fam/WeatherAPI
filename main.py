from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)  # a convention in flask

stations = pd.read_csv("data_small/stations.txt", skiprows=17)
stations = stations[['STAID', 'STANAME                                 ']]


@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())


@app.route("/api/v1/<weather_station>/<date>")  # <> special syntax for url we use in flask
def station(weather_station, date):
    filename = "data_small/TG_STAID" + str(weather_station).zfill(6) + ".txt"  # stations nr is extended to 6 digits by zeros
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    # csv_date = f"{date[0:4]}-{date[4:6]}-{date[6:]}" if we wanted to add dashes for user
    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10
    return {"station": weather_station,
            "date": date,
            "temperature": temperature}


@app.route("/api/v1/<weather_station>")
def all_data(weather_station):
    filename = "data_small/TG_STAID" + str(weather_station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    result = df.to_dict(orient="records")  # we put the whole dataframe into dictionary
    return result


@app.route("/api/v1/annual/<weather_station>/<year>")
def yearly(weather_station, year):
    filename = "data_small/TG_STAID" + str(weather_station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20)
    df['    DATE'] = df['    DATE'].astype(str)  # convert numbers to str
    result = df[df['    DATE'].str.startswith(str(year))].to_dict(orient="records")
    return result


if __name__ == "__main__":
    app.run(debug=True)  # we only run this app if this script is ran directly
    # not when we say, import this script somewhere, that way in place where
    # we import to we will not run this script but be able to use its functions

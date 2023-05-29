from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)  # a convention in flask


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/api/v1/<station>/<date>")  # <> special syntax for url we use in flask
def station(weather_station, date):
    temperature = 23
    return {"station": weather_station,
            "date": date,
            "temperature": temperature}


if __name__ == "__main__":
    app.run(debug=True)  # we only run this app if this script is ran directly
    # not when we say, import this script somewhere, that way in place where
    # we import to we will not run this script but be able to use its functions

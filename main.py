from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

stations = pd.read_csv("data_small/stations.txt", skiprows=17)
#  limit data to these 2 columns:
stations = stations[["STAID", "STANAME                                 "]]


@app.route("/home")
def home():
    return render_template("home.html", data=stations.to_html())


@app.route("/api/v1/<station>/<date>")
def station_data_by_date(station, date):
    #  zfill pads the value with 0s to the length specified
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df["    DATE"] == date]["   TG"].squeeze() / 10
    return {"station": station,
            "date": date,
            "temperature": temperature}


@app.route("/api/v1/yearly/<station>/<year>")
def station_data_by_year(station, year):
    #  zfill pads the value with 0s to the length specified
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    df["DATE"] = df["    DATE"].astype(str)
    result = df[df["DATE"].str.startswith(str(year))].to_dict(orient="records")
    return result

@app.route("/api/v1/<station>")
def all_data_by_station(station):
    #  zfill pads the value with 0s to the length specified
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    result = df.to_dict(orient="records")
    return result


if __name__ == "__main__":
    app.run(debug=True, port=5001)

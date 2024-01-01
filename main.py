from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

stations = pd.read_csv("data_small/stations.txt", skiprows=17)
#  limit data to these 2 columns:
stations = stations[["STAID","STANAME                                 "]]
@app.route("/home")
def home():
    return render_template("home.html", data=stations.to_html())

@app.route("/api/v1/<station>/<date>")
def about(station, date):
    #  zfill pads the value with 0s to the length specified
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df["    DATE"] == date]["   TG"].squeeze() / 10
    # temperature = df.station(date)
    # return render_template("about.html")
    return {"station": station,
            "date": date,
            "temperature": temperature}

if __name__ == "__main__":
    app.run(debug=True, port=5001)

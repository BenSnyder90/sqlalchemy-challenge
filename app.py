import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """Home page. List of all available routes"""
    return (
        f"<strong>Available routes:</strong><br/>"
        f"<b>/api/v1.0/precipitation</b><br/>"
        f"Returns a JSON dictionary of the date as the key and precip amount as the value<br/><br/>"
        f"<b>/api/v1.0/stations</b><br/>"
        f"Returns a JSON list of stations from the dataset<br/><br/>"
        f"<b>/api/v1.0/tobs</b><br/>"
        f"Returns a JSON list of temperature observations (TOBS) for the previous year<br/><br/>"
        f"<b>/api/v1.0/start</b> or <b>/api/v1.0/start/end</b><br/>"
        f"Returns a JSON list of the min temp, average temp, and the max temp for a given start date or start-end date range."
    )

@app.route("/api/v1.0/precipitation")
def precip():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23")
    session.close()
    prcp_dict = {}

    for date, prcp in results:
        prcp_dict[f"{date}"] = prcp

    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def station_count():
    session = Session(engine)
    results = session.query(Measurement.station).distinct()
    session.close()

    station_list = list(results)
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = 
    return(

    )

@app.route("/api/v1.0/<start>")
def temp_start(start):
    return(

    )

@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start, end):
    return(

    )

if __name__ == '__main__':
    app.run(debug=True)

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
        f"Returns a JSON list of temperature observations (TOBS) for the previous year for the most active station, USC00519281, Waihee 837.5.<br/><br/>"
        f"<b>/api/v1.0/start</b> or <b>/api/v1.0/start/end</b><br/>"
        f"Returns a JSON list of the min temp, average temp, and the max temp for a given start date or start-end date range, written as YYYY-MM-DD.<br/>"
        f"**Latest date in data is 2017-08-23**"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    print(f"Fetching the precipitation data for the last year of data")
    session = Session(engine)

    #Queries the date and prcp columns using the filter of the date taken from the Jupyter Notebook file
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23")
    session.close()

    #Create a dictionary to JSONIFY 
    prcp_dict = {}

    #Uses a for loop to run through the query and place each result in a new line in the dictionary
    #The date is the key and prcp value is the value in each dictionary listing
    for date, prcp in results:
        prcp_dict[f"{date}"] = prcp

    #Utilizes JSONIFY to return the dictionary
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def station_count():
    print(f"Fetching the unique station count")
    session = Session(engine)

    #Uses the distinct() function to get the unique stations
    results = session.query(Measurement.station, Station.name).\
                filter(Measurement.station == Station.station).distinct()
    session.close()

    #Stores the results in a jsonify-able list, then returns the station ID and names
    station_list = list(results)
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    print(f"Fetching the tobs data for the last year of data in station USC00519281")
    session = Session(engine)
    
    #Queries the date and TOBS data for the station with the most activity as found in the notebook
    #Gets the data for the last year in the data set
    results = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.station == "USC00519281").filter(Measurement.date >= "2016-08-23").all()

    session.close()

    #Create an empty temperature list to JSONIFY
    temp_list = []

    #Uses a for loop to run through the results and stores the date and TOBS data
    #in dictionary values. Adds them to the list in each iteration
    for date, tobs in results:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        temp_list.append(temp_dict)

    #Jsonifies the created list to return the date and TOBS value
    return jsonify(temp_list)

@app.route("/api/v1.0/<start>")
def temp_start(start):
    print(f"Fetching the aggregate tobs data at the start date of {start}")
    session = Session(engine)
    #Uses a Try/Except to see if the value put in the API corresponds to a date value in the table
    try:
        #Uses aggregate func functions to get the min, avg, and max of the data starting from
        #the entered date
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
                            func.max(Measurement.tobs)).filter(Measurement.date >= start )
        session.close()

    #####################################
    #Trying to print out labels TMIN, TAVG,
    #and TMAX to correspond with the aggregate data in the JSONified file.
    #Still working on this part
    #####################################

    #print(session.execute(results))

        #Turns the aggregate results into a list
        agg_list = list(results)
        
        #Checks if the list produced numeric results (can include 0)
        print("Checking if date is in data")
        if not all(map(lambda x: all(x), agg_list)) == True:
            return jsonify({"error": f"Date {start} not found"}), 404

        #print(agg_list[0])
    #agg_keys = ["TMIN","TAVG","TMAX"]
    #print(agg_list)
    #print(agg_keys)
    #agg_dict = dict(zip(agg_keys,agg_list))

        #Returns the JSONified list of the aggregate values
        print(f"TMIN, TAVG, and TMAX of {agg_list}, respectively")
        return jsonify(agg_list)
    
    #If the start date in the URL throws any error, returns a JSONified error
    except:
        return jsonify({"error": f"Date {start} not found"}), 404


@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start, end):
    print(f"Fetching the aggregate tobs data at the start date of {start} and end date of {end}")
    session = Session(engine)

    ######################################
    #Trying to print out labels for TMIN, TAVG,and TMAX
    #And running checks if the date range is actually in the data.
    #One test searching for a start date within the data and an end date
    #outside of the date range resulted in a successful JSON creation.
    #Need to finish this code
    ######################################

    #start_in_data = False
    #end_in_data = False

    # while start_in_data == False:
    #     for x in Measurement:
    #         if start == x.date:
    #             start_in_data = True
    #             for y in Measurement:
    #                 if end == y.date:
    #                     end_in_data = True
    #Uses a Try/Except to see if the value put in the API corresponds to a date range in the table
    try:

    #Uses similar query syntax as in the notebook to find the aggregate data of the date range
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
        func.max(Measurement.tobs)).filter(Measurement.date <=\
        end) .filter(Measurement.date >= start)
        session.close()
        
        #Saves the results into a list to JSONIFY
        agg_list = list(results)

        #Checks if the list produced numeric results (can include 0)
        print("Checking if date is in data")
        if not all(map(lambda x: all(x), agg_list)) == True:
            return jsonify({"error": f"Date range not found"}), 404

        #Returns the JSONIFied list of aggregate data
        print(f"TMIN, TAVG, and TMAX of {agg_list}, respectively")
        return jsonify(agg_list)
        

    #If the start date or end date in the URL throws any error, returns a JSONified error
    except:
        return jsonify({"error": f"Date range not found"}), 404

#Launches the app via the terminal
if __name__ == '__main__':
    app.run(debug=True)

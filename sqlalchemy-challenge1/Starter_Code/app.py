# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect


from flask import Flask, jsonify



#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`

Measurement = Base.classes.measurement
Station = Base.classes.station  

# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        "/api/v1.0/{start}<br/>"
        "/api/v1.0/{start}/{end}<br/>"

)

@app.route("/api/v1.0/precipitation")
def prcp():
    year_later = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_later).all()
    cleandata = {}
    for date, prcp in results:
        cleandata[date] = prcp 
    session.close()
    return jsonify(cleandata)

@app.route("/api/v1.0/stations")
def stationlist():
    station_list = []
    list = session.query(Station).order_by(Station.station).all()
    for station in list:
        station_list.append({
            'Station': station.station
        })
    session.close()
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def most_active():
    most_active = []
    year_later = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    top_station = 'USC00519281'
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= year_later).filter(Measurement.station == top_station).all()
    for date, tobs in results:
        most_active.append({
            'Date': date,
            'Temperature': tobs 
        })
    session.close()
    return jsonify(most_active)


@app.route('/api/v1.0/<start>')
def get_temperatures_start(start):
    results = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start).first()
    session.close()
    
    # Create a dictionary to hold the results
    temperature_data = {
        "TMIN": results[0],
        "TAVG": results[1],
        "TMAX": results[2]
    }
    
    return jsonify(temperature_data)

@app.route('/api/v1.0/<start>/<end>')
def get_temperatures_start_end(start, end):
    results = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start).filter(Measurement.date <= end).first()
    session.close()
    
    # Create a dictionary to hold the results
    temperature_data = {
        "TMIN": results[0],
        "TAVG": results[1],
        "TMAX": results[2]
    }
    return jsonify(temperature_data)


if __name__ == '__main__':
    app.run(debug=True)
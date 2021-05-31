# import Flask
from flask import Flask, jsonify

# Create an app, being sure to pass __name__
app = Flask(__name__)

# Import Dependencies and Setup
import numpy as np
import datetime as dt

# Python SQL Toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.pool import StaticPool

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={"check_same_thread": False}, poolclass=StaticPool, echo=True)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# Create our session (link) from Python to the DB
session = Session(engine)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
        # Convert the Query Results to a Dictionary Using `date` as the Key and `prcp` as the Value
        # Finding out the date twelve months before the last date
        twelve_months_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
        # Perform a query to retrieve the data and precipitation scores
        last_months_prcp = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date >= twelve_months_ago).\
                order_by(Measurement.date).all()
        # Converting List of Tuples Into a Dictionary
        last_months_prcp_list = dict(last_months_prcp)
        # Returning JSON Representation of Dictionary
        return jsonify(last_months_prcp_list)

@app.route("/api/v1.0/stations")
def stations():
        # Return a JSON List of Stations From the Dataset
        stations = session.query(Station.station, Station.name).all()
        # Converting List of Tuples Into  List
        stations_list = list(stations)
        # Returning JSON List of Stations from the Dataset
        return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
        # Finding out the date twelve months before the last date
        twelve_months_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
        # Designing a Query to Retrieve the Last 12 Months of Precipitation and Tobs values
        tobs = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= twelve_months_ago).\
                order_by(Measurement.date).all()
        # Converting List of Tuples Into Normal List
        tobs_list = list(tobs)
        # Return JSON List of Temperature Observations for the past twelve months
        return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start_range(start):
        start_range = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                group_by(Measurement.date).all()
        # Converting List of Tuples Into List
        start_range_list = list(start_range)
        # Returning JSON List of Min Temp, Avg Temp and Max Temp for a Given Start Range
        return jsonify(start_range_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end_range(start, end):
        start_end_range = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).\
                group_by(Measurement.date).all()
        # Converting List of Tuples Into Normal List
        start_end_range_list = list(start_end_range)
        # Returning JSON List of Min Temp, Avg Temp and Max Temp for a Given Start-End Range
        return jsonify(start_end_range_list)

if __name__ == '__main__':
    app.run(debug=True)
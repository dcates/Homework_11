from sqlalchemy import create_engine, func
from django.db.models import Avg, Max, Min, Sum
from flask import Flask, jsonify
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Query for the dates and temperature observations from the last year"""
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2017-01-01').all()

    """Convert the query results to a Dictionary using date as the key and tobs as the value.
"""
    dictionary = []
    for measurement in results:
        measurement_dict = {}
        measurement_dict["date"] = measurement.date
        measurement_dict["tobs"] = measurement.tobs
        dictionary.append(measurement_dict)

    """Return the json representation of your dictionary."""
    return jsonify(dictionary)

@app.route("/api/v1.0/stations")
def stations():
    """Return a json list of stations from the dataset"""
    results = session.query(Stations.station).group_by(Stations.station).all()

    """convert list of tuples into normal list"""
    all_stations = list(np.ravel(results))

    """jsonify"""
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temperatures():
    """Return a json list of Temperature Observations (tobs) for the previous year"""
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2017-01-01').all()
   
    """convert list of tuples into normal list"""
    temps = list(np.ravel(results))

    """jsonify"""
    return jsonify(temps)

@app.route("/api/v1.0/<start>")
def start():
    """TMIN"""
    results_min = session.query(Measurement.tobs).filter(Measurement.date >= start).all().aggregate(Min('tobs'))
    """convert list of tuples into normal list"""
    tmin = list(np.ravel(results_min))
    """jsonify"""
    return jsonify(tmin)

    """TAVG"""
    results_avg = session.query(Measurement.tobs).filter(Measurement.date >= start).all().aggregate(Avg('tobs'))
    """convert list of tuples into normal list"""
    tavg = list(np.ravel(results_avg))
    """jsonify"""
    return jsonify(tavg)

    """TMAX"""
    results_avg = session.query(Measurement.tobs).filter(Measurement.date >= start).all().aggregate(Max('tobs'))
    """convert list of tuples into normal list"""
    tmax = list(np.ravel(results_max))
    """jsonify"""
    return jsonify(tmax)

@app.route("/api/v1.0/<start>/<end>")
def start():
    """TMIN"""
    results_min = session.query(Measurement.tobs).filter(Measurement.date >= start).filter(Measurement.date < end).all().aggregate(Min('tobs'))
    """convert list of tuples into normal list"""
    tmin = list(np.ravel(results_min))
    """jsonify"""
    return jsonify(tmin)

    """TAVG"""
    results_avg = session.query(Measurement.tobs).filter(Measurement.date >= start).filter(Measurement.date < end).all().aggregate(Avg('tobs'))
    """convert list of tuples into normal list"""
    tavg = list(np.ravel(results_avg))
    """jsonify"""
    return jsonify(tavg)

    """TMAX"""
    results_max = session.query(Measurement.tobs).filter(Measurement.date >= start).filter(Measurement.date < end).all().aggregate(Max('tobs'))
    """convert list of tuples into normal list"""
    tmax = list(np.ravel(results_max))
    """jsonify"""
    return jsonify(tmax)

if __name__ == '__main__':
    app.run(debug=True)
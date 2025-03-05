# Import the dependencies.
from flask import Flask , jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(autoload_with = engine)

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
def home():
    return (
        f"Welcome to the Hawaii Flask API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2016-08-23<br/>"
        f"/api/v1.0/2016-08-23/2017-08-23"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    return 'this is a test'

@app.route("/api/v1.0/stations")
def stations():

    stationsquery = session.query(Station.station).all()
    stationdict = {}
    for idx , station in enumerate(stationsquery):
        stationdict[f"Station {idx}"] = station[0]
    
    return jsonify(stationdict)

@app.route("/api/v1.0/tobs")
def tobs():
    Q = [Measurement.date , Measurement.tobs]
    dto = session.query(*Q).filter(Measurement.date >= '2016-08-23').filter(Measurement.station == 'USC00519281').all()
    dtodict = {}
    for row in dto:
        (date , tobs) = row
        dtodict[date] = tobs
    
    return jsonify(dtodict)

if __name__ == "__main__":
    app.run(debug=True)
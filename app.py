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
    sel = [Measurement.date , Measurement.prcp]
    query = session.query(*sel).filter(Measurement.date >= '2016-08-23').all()
    retdict = {}
    for row in query:
        
        (date , prcp) = row
        if prcp != None:
            retdict[date] = prcp

    return jsonify(retdict)

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




@app.route("/api/v1.0/<start>")
def tempcalc(start):
    T = [func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)]
    tempquery = session.query(*T).filter(Measurement.date >= start).all()
    tempdict = {}
    (tmin , tavg , tmax) = tempquery[0]
    tempdict["TMIN"] = tmin
    tempdict["TAVG"] = tavg
    tempdict["TMAX"] = tmax

    return jsonify(tempdict)

@app.route("/api/v1.0/<start>/<end>")
def tempcalc2(start,end):
    T2 = [func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)]
    temp2query = session.query(*T2).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temp2dict = {}
    (t2min , t2avg , t2max) = temp2query[0]
    temp2dict["TMIN"] = t2min
    temp2dict["TAVG"] = t2avg
    temp2dict["TMAX"] = t2max

    return jsonify(temp2dict)

if __name__ == "__main__":
    app.run(debug=True)
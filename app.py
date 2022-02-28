import numpy as np
import pandas as pd
import datetime as dt
from datetime import datetime, timedelta
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station


app=Flask(__name__)


@app.route("/")
def home():
    print("Server received request")
    return (f"Welcome to my page<br/>"
            f"Available routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/<start><br/>"
            f"/api/v1.0/<start>/<end><br/>")
            

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    year_ago_data=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > '2016-08-22')
    year_ago_data_df=pd.DataFrame(year_ago_data, columns=['date','prcp'])
    index_date=year_ago_data_df.set_index('date')
    session.close()
    precipitation=list(np.ravel(index_date))
    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)
    total_stations=session.query(Station.station).all()
    session.close()
    stations_list=list(np.ravel(total_stations))
    return jsonify(stations_list)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    year_ago_active = dt.date(2017,8,18) - dt.timedelta(days=365)
    year_ago_data_active=session.query(Measurement.date, Measurement.tobs).filter(Measurement.station=='USC00519281').filter(Measurement.date > '2016-08-18')
    year_ago_data_active_df=pd.DataFrame(year_ago_data_active, columns=['date','tobs'])
    session.close()
    tobs_list=list(np.ravel(year_ago_data_active_df))
    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>")
def start():
    session = Session(engine)
    lowest_temp=session.query(func.min(Measurement.tobs)).filter(Measurement.station=='USC00519281').all()
    print(f"The lowest temperature was {lowest_temp}.")
    highest_temp=session.query(func.max(Measurement.tobs)).filter(Measurement.station=='USC00519281').all()
    print(f"The highest temperature was {highest_temp}.")
    avg_temp=session.query(func.avg(Measurement.tobs)).filter(Measurement.station=='USC00519281').all()
    print(f"The average temperature was {avg_temp}.")
    session.close()

    return("")


@app.route("/api/v1.0/<start>/<end>")
def end():
    return("")


if __name__ =="__main__":
    app.run(debug=True)


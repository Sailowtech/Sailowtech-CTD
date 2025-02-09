from fastapi import FastAPI
from starlette.responses import StreamingResponse

from software.sailowtech_ctd.database import db
from pony.orm import *
from software.sailowtech_ctd.database.measurement import Measurement
from software.sailowtech_ctd.database.run import Run
import io
import csv

app = FastAPI()


@app.get("/")
def root():
    """
    Welcome message of the web service. Can be used to check if the service is running.

    :return: Returns a welcome message in a JSON
    """
    return {"data": "Welcome to the CTD"}

@app.get("/runs")
def get_runs():
    """
    Fetch a list of all the runs.

    :return: Returns the runs as a list in the data-property
    """
    with db_session:
        return {'data': [p.to_dict() for p in list(Run.select())]}

@app.get("/csv")
def csv_export():
    """
    Export measurements to a CSV-file. Can be filtered.

    :return: Returns the measurements as a CSV
    """
    with db_session:
        measurements = select((m.run.id, m.timestamp, m.value, m.sensor.name) for m in Measurement)[:]
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["run_id", "value", "timestamp", "sensor_name"])
        for m in measurements: writer.writerow(m)
        output.seek(0)
        return StreamingResponse(
            output,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=measurements.csv"}
        )
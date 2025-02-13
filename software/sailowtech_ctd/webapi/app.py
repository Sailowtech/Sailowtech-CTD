from fastapi import FastAPI

from starlette.responses import StreamingResponse
from starlette.staticfiles import StaticFiles

from software.sailowtech_ctd.database import db
from pony.orm import *
from software.sailowtech_ctd.database.measurement import Measurement
from software.sailowtech_ctd.database.run import Run, create_run, RunTypes, stop_run
import io
import csv

app = FastAPI()

@app.get("/root")
def root():
    """
    Welcome message of the web service. Can be used to check if the service is running.

    :return: Returns a welcome message in a JSON
    """
    return {"data": "Welcome to the CTD"}

@app.get("/run")
def run(run_type: RunTypes, run_data: int = 0):
    """
    Create a new run and measure. Why are you running?
    Run Types:
    - 0: Manual stopping
    - 1: Stop after amount of seconds (run_data)
    - 2: Stop after amount of measurements (specified in run_data)
    :return: Returns the id of the run upon finish.
    """
    return create_run(run_type, run_data)

@app.get("/stop")
def stop(run_id: int) -> bool:
    """
    Stop the run for the given run id
    :return: Returns true if finished successfully
    """
    return stop_run(run_id)

@app.get("/runs")
def get_runs():
    """
    Fetch a list of all the runs.

    :return: Returns the runs as a list in the data-property
    """
    with db_session:
        return {'data': [p.to_dict() for p in list(Run.select())]}

@app.get("/csv")
def csv_export(run_id: int | None = None):
    """
    Export measurements to a CSV-file. Can be filtered.

    :return: Returns the measurements as a CSV
    """
    with db_session:
        measurements = select((m.run.id, m.timestamp, m.value, m.sensor.name) for m in Measurement)
        if run_id is None:
            measurements = measurements[:]
        else:
            measurements = measurements.filter(lambda r, a, b, c: r == run_id)

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


app.mount("/", StaticFiles(directory="software/sailowtech-ctd-frontend/dist", html=True), name="frontend")
import time
import datetime
import os
import pathlib
from errno import EPERM

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from peewee import fn, Case
from starlette.responses import StreamingResponse
from starlette.staticfiles import StaticFiles

from software.sailowtech_ctd.logger import logger
from software.sailowtech_ctd.database.measurement import Measurement
from software.sailowtech_ctd.database.run import Run, create_run, RunTypes, stop_run
import io
import csv
from pydantic import BaseModel

from software.sailowtech_ctd.database.sensor import Sensor


class TimestampRequest(BaseModel):
    timestamp: int


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/root")
def root():
    """
    Welcome message of the web service. Can be used to check if the service is running.

    :return: Returns a welcome message in a JSON
    """
    return {"data": "Welcome to the CTD", "success": True}

@app.get("/system-time")
def system_time():
    """
    Get the current system-time. Can be used to check if synchronization is necessary.

    :return: Returns the current timestamp in data.system-time
    """
    return {"data": {"system_time": datetime.datetime.now()}, "success": True}

@app.post("/system-time")
def system_time(request: TimestampRequest):
    """
    Set the system time. Used to synchronize the time if the device has no internet access
    :param request: Timestamp as Unix epoch
    :return: Returns true in success if it was set successfully
    """
    timestamp = request.timestamp
    logger.info(f"Attempting to set system time to {timestamp}")
    try:
        time.clock_settime(time.CLOCK_REALTIME , timestamp)
        return {"success": True}
    except:
        logger.error("Unable to set system time because of missing privileges. Not running with systemd?")
        return {"success": False}

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
    return {'data': list(Run.select().dicts())}

@app.get("/sensors")
def get_sensors():
    """
    Fetch a list of all the runs.

    :return: Returns the runs as a list in the data-property
    """
    return {'data': list(Sensor.select().dicts())}

@app.get("/visualization-data")
def get_visualization_data(run_id: int):
    """
    Fetch the data of a run for the visualization

    :return: Returns the data of a run for visualization
    """
    sensors = Sensor.select()
    aggregates = [
        fn.SUM(Case(None, [(Measurement.sensor == sensor, Measurement.value)], None)).alias(sensor.metric.name)
        for sensor in sensors
    ]
    query = Measurement.select(
        Measurement.timestamp, *aggregates
    ).where(Measurement.run == run_id).group_by(Measurement.timestamp)

    chart_data = {"labels": [], "datasets": []}
    sensor_values = {}

    for row in query.dicts():
        timestamp = row.pop("timestamp")
        chart_data["labels"].append(timestamp)

        for sensor, value in row.items():
            if sensor not in sensor_values:
                sensor_values[sensor] = []
            sensor_values[sensor].append(value)

    for sensor, values in sensor_values.items():
        chart_data["datasets"].append({"label": sensor, "data": values})

    return chart_data

@app.get("/csv")
def csv_export(run_id: int | None = None):
    """
    Export measurements to a CSV-file. Can be filtered.

    :return: Returns the measurements as a CSV
    """
    measurements = Measurement.select(Measurement.run, Measurement.timestamp, Measurement.value, Measurement.sensor)
    if run_id is None:
        measurements = measurements
        headers = {f"Content-Disposition": "attachment; filename=measurements.csv"}
    else:
        measurements = measurements.where(Measurement.run == run_id)
        headers = {f"Content-Disposition": f"attachment; filename=Measurements_Run_{run_id}_{Run.get(id=run_id).timestamp.strftime('%d.%m.%Y_%H%M')}.csv"}

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["run_id", "timestamp", "value", "sensor_name"])
    for m in measurements: writer.writerow((m.run.id, m.timestamp, m.value, m.sensor.name))
    output.seek(0)
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers=headers
    )

directory = os.path.abspath(os.path.join(pathlib.Path(os.path.dirname(__file__), "../../sailowtech-ctd-frontend/dist")))
print(directory)
app.mount("/", StaticFiles(directory=directory, html=True), name="frontend")
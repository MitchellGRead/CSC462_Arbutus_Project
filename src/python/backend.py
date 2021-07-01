import os
from flask import Flask, request, send_file
from datetime import datetime, timedelta
from PIL import ImageChops

from pull_sentinel_data import fetch_sentinel_data


"""
Run the dev server locally with the following bash commands:
 - cd src/python
 - 'export FLASK_APP=backend.py'
 - flask run OR pythonx.y -m flask run
"""
app = Flask(__name__)
@app.route("/satellite/aerosol", methods=['GET'])
async def get_aerosol_data():
    # grab request params
    today = datetime.today()
    bout_a_week_ago = datetime.today() - timedelta(days=7)

    sentinel_args = {
        "location": request.args.get("location", "EX"),
        "from_date": request.args.get("from_date", bout_a_week_ago.strftime("%Y-%m-%d")),
        "to_date": request.args.get("to_date", today.strftime("%Y-%m-%d"))
    }

    # TODO: can we do fetch these concurrently? or batch them?
    # fetch NDVI
    sentinel_args["evalscript"] = "NDVI"
    nvdi = fetch_sentinel_data(kwargs=sentinel_args, return_image=True)

    # fetch AFVI
    sentinel_args["evalscript"] = "AFVI"
    afvi = fetch_sentinel_data(kwargs=sentinel_args, return_image=True)

    # TODO: revisit index consolidation
    diff = ImageChops.difference(nvdi, afvi)

    path = "tmp/diff.tiff"
    diff.save(path)

    # client download
    download = send_file(path, as_attachment=True)
    os.remove(path)
    return download

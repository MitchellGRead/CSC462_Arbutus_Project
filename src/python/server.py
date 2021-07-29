import os
from flask import Flask, request, send_file
from datetime import datetime, timedelta
from PIL import Image
import json

from pull_sentinel_data import fetch_sentinel_data
from plot_sentinel_data import plot_image


"""
Run the dev server locally with the following bash commands:
 - cd src/python
 - 'export FLASK_APP=server.py'
 - flask run OR pythonx.y -m flask run
"""
app = Flask(__name__)
@app.route("/plot/heatmap", methods=['POST'])
async def plot_heatmap():
    # grab request params
    heatmap = request.files["heatmap"]
    heatmap = Image.open(heatmap.stream)

    coordinates = request.files["coords"]
    coordinates.save("coords.json")
    with open("coords.json") as fp:
        coordinates = json.load(fp)

    if coordinates is None:
        print("[ERR] server did not recieve coordinates.")
        return

    today = datetime.today()
    bout_a_week_ago = datetime.today() - timedelta(days=7)

    sentinel_args = {
        "coords": coordinates,
        "from_date": request.args.get("from_date", bout_a_week_ago.strftime("%Y-%m-%d")),
        "to_date": request.args.get("to_date", today.strftime("%Y-%m-%d"))
    }

    # fetch colour image
    sentinel_args["evalscript"] = "COLOUR"
    colour = fetch_sentinel_data(kwargs=sentinel_args, return_image=True)

    # plot image
    print(f"[DEBUG] Plotting heatmap...")
    plotted_image = plot_image(colour, heatmap)

    path = "plotted.tiff"
    plotted_image.save(path)
    # client download
    download = send_file(path, as_attachment=True)
    os.remove(path)
    os.remove("coords.json")

    return download

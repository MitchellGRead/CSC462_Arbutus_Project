import argparse
import datetime
import os
import json
import math
import random
from numpy import absolute
import requests

from numpy.random import normal
import geoplot
import geoplot.crs as gcrs
import geopandas
import matplotlib.pyplot as plt


def call_server():
	args = get_args()

	# load in geojson
	here = os.path.dirname(os.path.realpath('__file__'))
	filename = os.path.join(here, f'datasets/{args.dataset}.json')
	geojson_dict = None

	with open(filename, "r") as geojson:
		geojson_dict = json.load(geojson)

	if not geojson_dict:
		print(f"[ERR] Could not load {args.dataset} with path: {filename}.")
		return

	coords = geopandas.read_file(os.path.join(here, f'datasets/{args.coords}.json'))

	# add noise if desired
	if args.noise > 0:
		add_noise(args.noise, geojson_dict)

	# duplicate points based on their 'value' for visualization purposes
	duplicates = []
	for feature in geojson_dict["features"]:
		value = int(feature["properties"]["value"])
		duplicates.extend([
			feature for _ in range(value)
		])

	geojson_dict["features"].extend(duplicates)

	# reload data
	with open("temp.json", "w") as geojson:
		geojson.write(json.dumps(geojson_dict))

	dataset = geopandas.read_file("temp.json")
	os.remove("temp.json")

	# aggregate into heatmap
	ax = geoplot.polyplot(coords, projection=gcrs.AlbersEqualArea())
	geoplot.kdeplot(dataset, cmap='Reds', shade=True, ax=ax)

	plt.savefig("temp.tiff", bbox_inches="tight")

	# call server
	url = "http://127.0.0.1:5000/plot/heatmap"
	files = {
		"coords": ("coords.json", open(f'datasets/{args.coords}.json', "rb"), "application/json"),
		"heatmap": ("heatmap.tiff", open("temp.tiff", "rb"), "image/tiff")
	}

	with requests.post(url, files=files, stream=True) as resp:
		resp.raise_for_status()

		with open("returned.tiff", "wb") as fp:
			for chunk in resp.iter_content(chunk_size=8192):
				fp.write(chunk)

	os.remove("temp.tiff")

def add_noise(noise, geojson):
	"""
	Add noise to point values after finding average and standard deviation.
	"""
	values = []
	for feature in geojson["features"]:
		values.append(feature["properties"]["value"])

	avg = sum(values) / len(values)

	deviation = 0
	for val in values:
		deviation += (val - avg) ** 2

	deviation /= len(values)
	deviation = deviation ** (1/2)

	for val, feature in zip(values, geojson["features"]):
		dice_roll = random.random()
		absolute_noise = deviation * dice_roll * noise / 100

		if dice_roll >= 0.5:
			feature["properties"]["value"] = round(val + absolute_noise)
		else:
			feature["properties"]["value"] = round(val - absolute_noise)


def get_args():
	""" Configure and fetch script args """
	parser = argparse.ArgumentParser()

	parser.add_argument(
        "--dataset",
        required=True,
		help="A geojson file containing points with 'value' properties between 1-10."
    )
	parser.add_argument(
        "--bbox",
        required=True,
		help="A geojson file containing a polygon of points which describes the bounding box of the dataset."
    )
	parser.add_argument(
		"--mime",
		choices=[
			"PNG", "JPEG", "TIFF"
		],
		default="TIFF"
	)
	parser.add_argument(
		"--noise",
		type=int,
		choices=[i for i in range(101)],
		default=0,
		help="A value between 0-100 indicating the percentage of noise added to the dataset."
	)

	return parser.parse_args()

if __name__ == "__main__":
	call_server()

import argparse
import datetime

from sentinelhub import (
	BBox,
	CRS,
	SHConfig,
	MimeType,
	SentinelHubRequest,
	DataCollection,
	bbox_to_dimensions,
)
from PIL import Image

import constants

def fetch_sentinel_data(kwargs=None, return_image=True):
	""" 
	Fetch satellite data.
	If 'kwargs' is None the arguments will be fetched via arg parsing.
	If 'return_image' is True the fetched image will be returned to the caller.
	Otherwise, the image will be saved locally.
	"""
	args = get_args() if not kwargs else kwargs

	evalscript = args.get("evalscript", "COLOUR")
	from_date = str(args.get("from_date"))
	to_date = str(args.get("to_date"))
	mime = args.get("mime", "TIFF")

	if hasattr(args, "location"):
		bbox_points = getattr(constants, args.location)
	else:
		bbox_points = coords_to_bbox(args.get("coords"))

	bbox = BBox(bbox=bbox_points, crs=CRS.WGS84)

	config = SHConfig()

	config.instance_id = constants.INSTANCE_ID
	config.client_id = constants.CLIENT_ID
	config.client_secret = constants.CLIENT_SECRET

	config.save()

	# TODO: bust up time interval into months and make separate requests
	request = SentinelHubRequest(
		evalscript=getattr(constants, evalscript),
		input_data=[
			SentinelHubRequest.input_data(
				data_collection=DataCollection.SENTINEL2_L1C,
				time_interval=(from_date, to_date),
			)
		],
		responses=[
			SentinelHubRequest.output_response('default', getattr(MimeType, mime))
		],
		bbox=bbox,
		size=bbox_to_dimensions(bbox, resolution=constants.RESOLUTION),
		config=config
	)

	images = request.get_data()
	for idx, image in enumerate(images):
		im = Image.fromarray(image)
		
		if return_image:
			return im

		im.save(f"../../satellite_data/{args.location}-{args.evalscript}-{idx}.{args.mime.lower()}")

def coords_to_bbox(coords):
	# order is min(lat), min(long), max(lat), max(long)
	min_lat, min_long, max_lat, max_long = 90, 180, -90, -180
	for coords in coords["features"][0]["geometry"]["coordinates"][0]:
		lng, lat = coords
		min_lat = min(lat, min_lat)
		min_long = min(lng, min_long)
		max_lat = max(lat, max_lat)
		max_long = max(lng, max_long)

	return [min_long, min_lat, max_long, max_lat]

def get_args():
	""" Configure and fetch script args """
	parser = argparse.ArgumentParser()

	parser.add_argument(
		"--location",
		choices=["VAN", "KAMLOOPS", "OKANAGAN", "EX"],
		required=True
	)
	parser.add_argument(
		"--from_date",
		type=datetime.date.fromisoformat,
		help="date format: YYYY-MM-DD",
		required=True
	)
	parser.add_argument(
		"--to_date",
		type=datetime.date.fromisoformat,
		help="date format: YYYY-MM-DD",
		required=True
	)
	parser.add_argument(
		"--mime",
		choices=[
			"PNG", "JPEG", "TIFF"
		],
		required=True
	)
	parser.add_argument(
		"--evalscript",
		choices=["NDVI", "AFVI", "COLOUR"],
		default="COLOUR"
	)

	return vars(parser.parse_args())

if __name__ == "__main__":
	fetch_sentinel_data()

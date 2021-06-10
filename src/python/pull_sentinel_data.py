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

def fetch_data():
	""" Fetch satellite data """
	args = get_args()

	cords = getattr(constants, args.location)
	bbox = BBox(bbox=cords, crs=CRS.WGS84)

	config = SHConfig()

	config.instance_id = constants.INSTANCE_ID
	config.client_id = constants.CLIENT_ID
	config.client_secret = constants.CLIENT_SECRET

	config.save()

	# TODO: bust up time interval into months and make separate requests
	request = SentinelHubRequest(
		evalscript=getattr(constants, args.evalscript),
		input_data=[
			SentinelHubRequest.input_data(
				data_collection=DataCollection.SENTINEL2_L1C,
				time_interval=(str(args.from_date), str(args.to_date)),
			)
		],
		responses=[
			SentinelHubRequest.output_response('default', getattr(MimeType, args.mime))
		],
		bbox=bbox,
		size=bbox_to_dimensions(bbox, resolution=constants.RESOLUTION),
		config=config
	)

	images = request.get_data()
	for idx, image in enumerate(images):
		im = Image.fromarray(image)
		im.save(f"../../satellite_data/{args.location}-{args.evalscript}-{idx}.{args.mime.lower()}")

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

	return parser.parse_args()

if __name__ == "__main__":
	fetch_data()

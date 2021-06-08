from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import json
import requests
import os
import datetime
import numpy as np
import matplotlib.pyplot as plt

from sentinelhub import SHConfig
from sentinelhub import MimeType, CRS, BBox, SentinelHubRequest, SentinelHubDownloadClient, \
	DataCollection, bbox_to_dimensions, DownloadRequest

from utils import plot_image

# Bounding Box coords for areas of interest
vancouver_bbox_cords = [-123.314506,49.007619,-122.189780,49.383633]
vancouver_resolution = 60
vancouver_bbox = BBox(bbox=vancouver_bbox_cords, crs=CRS.WGS84)
vancouver_size = bbox_to_dimensions(vancouver_bbox, resolution=vancouver_resolution)


kamloops_bbox = [-120.623619,50.626084,-120.124174,50.807054]
okanagan_bbox = [-119.887128,49.003343,-119.308973,49.224471]

evalscript_color = """
		//VERSION=3

		function setup() {
			return {
				input: ["B02", "B03", "B04"],
				output: {
					bands: 3
				}
			};
			}

		function evaluatePixel(sample) {
			return [sample.B04, sample.B03, sample.B02];
		}
"""


def main():
	config = SHConfig()

	config.instance_id='d6a7dc2f-2fbb-4786-a6cf-91a5e10e249a'
	config.client_id='91439487-66bd-4f7a-a6ad-29895c311a51'
	config.client_secret='U&5::8|HL%_SY&KOObGV&>s|6i&BR_QtdnW.E8]W'

	config.save()


	request_true_color = SentinelHubRequest(
		evalscript=evalscript_color,
		input_data=[
			SentinelHubRequest.input_data(
				data_collection=DataCollection.SENTINEL2_L1C,
				time_interval=('2020-06-12', '2020-06-13'),
			)
		],
		responses=[
			SentinelHubRequest.output_response('default', MimeType.PNG)
		],
		bbox=vancouver_bbox,
		size=vancouver_size,
		config=config
	)
	
	images = request_true_color.get_data()
	image = images[0]
	plot_image(image, factor=3.5/255, clip_range=(0,1))


if __name__ == '__main__':
	main()
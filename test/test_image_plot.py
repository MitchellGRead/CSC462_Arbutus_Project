from PIL import Image
from sentinelhub import MimeType, CRS, BBox, SentinelHubRequest, DataCollection, bbox_to_dimensions
from sentinelhub import SHConfig

# Bounding Box coords for areas of interest
# vancouver_bbox_cords=[46.16, -16.15, 46.51, -15.58] #as in example
vancouver_bbox_cords = [-123.31, 49.00, -122.18, 49.38] #actual van coords
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
			return [2.5*sample.B04, 2.5*sample.B03, 2.5*sample.B02];
		}
"""


def main():
	config = SHConfig()

	config.instance_id='d6a7dc2f-2fbb-4786-a6cf-91a5e10e249a'
	config.sh_client_id='91439487-66bd-4f7a-a6ad-29895c311a51'
	config.sh_client_secret='U&5::8|HL%_SY&KOObGV&>s|6i&BR_QtdnW.E8]W'

	config.save()

	from_date = '2020-06-04'
	to_date = from_date

	request_true_color = SentinelHubRequest(
		evalscript=evalscript_color,
		input_data=[
			SentinelHubRequest.input_data(
				data_collection=DataCollection.SENTINEL2_L1C,
				time_interval=(from_date, to_date),
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

	im = Image.fromarray(image)
	im.save('./images/van.jpeg')

	#png.from_array(image).save('van.png')
	#plot_image(image, factor=3.5/255, clip_range=(0,1))


if __name__ == '__main__':
	main()
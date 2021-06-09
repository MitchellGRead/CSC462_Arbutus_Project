""" module for constants """

EVALSCRIPT_COLOUR = """
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

CORDS_EX = [46.16, -16.15, 46.51, -15.58]
CORDS_KAMLOOPS = [-120.623619,50.626084,-120.124174,50.807054]
CORDS_VAN = [-123.31, 49.00, -122.18, 49.38]
CORDS_OKANAGAN = [-119.887128,49.003343,-119.308973,49.224471]

INSTANCE_ID = "d6a7dc2f-2fbb-4786-a6cf-91a5e10e249a"
CLIENT_ID = "91439487-66bd-4f7a-a6ad-29895c311a51"
CLIENT_SECRET = "U&5::8|HL%_SY&KOObGV&>s|6i&BR_QtdnW.E8]W"

RESOLUTION = 60

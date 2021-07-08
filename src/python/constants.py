""" module for constants """

COLOUR = """
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

AFVI = """
//VERSION=3
// Aerosol free vegetation index 1600  (abbrv. AFRI1600)
//
// General formula: (NIR-0.66*1600nm/(NIR + 0.66*1600nm)
// This is an auto-generated script. Double checking the source information with the URL below is recommended.
// URL https://www.indexdatabase.de/db/si-single.php?sensor_id=96&rsindex_id=393
//

let index = B08 - 0.66 * B11 / (B08 + 0.66 * B11);
let min = -0.9;
let max = 0.312;
let zero = 0.0;

// colorBlend will return a color when the index is between min and max and white when it is less than min.
// To see black when it is more than max, uncomment the last line of colorBlend.
// The min/max values were computed automatically and may be poorly specified, feel free to change them to tweak the displayed range.
// This index crosses zero, so a diverging color map is used. To tweak the value of the break in the color map, change the variable 'zero'.

let underflow_color = [1, 1, 1];
let low_color = [208/255, 88/255, 126/255];
let high_color = [241/255, 234/255, 200/255];
let zero_color = [0, 147/255, 146/255];
let overflow_color = [0, 0, 0];

return colorBlend(index, [min, min, zero, max],
[
	underflow_color,
	low_color,
	zero_color, // divergent step at zero
	high_color,
	//overflow_color // uncomment to see overflows
]);
"""

NDVI = """
//VERSION=3
// Normalized Difference MIR/NIR Normalized Difference Vegetation Index (in case of strong atmospheric disturbances) (abbrv. NDVI)
//
// General formula: (MIR - NIR) / (MIR + NIR)
// This is an auto-generated script. Double checking the source information with the URL below is recommended.
// URL https://www.indexdatabase.de/db/si-single.php?sensor_id=96&rsindex_id=59
//

let index = (B12 - B08) / (B12 + B08);
let min = -0.889;
let max = 0.892;
let zero = 0.0;

// colorBlend will return a color when the index is between min and max and white when it is less than min.
// To see black when it is more than max, uncomment the last line of colorBlend.
// The min/max values were computed automatically and may be poorly specified, feel free to change them to tweak the displayed range.
// This index crosses zero, so a diverging color map is used. To tweak the value of the break in the color map, change the variable 'zero'.

let underflow_color = [1, 1, 1];
let low_color = [208/255, 88/255, 126/255];
let high_color = [241/255, 234/255, 200/255];
let zero_color = [0, 147/255, 146/255];
let overflow_color = [0, 0, 0];

return colorBlend(index, [min, min, zero, max],
[
	underflow_color,
	low_color,
	zero_color, // divergent step at zero
	high_color,
	//overflow_color // uncomment to see overflows
]);
"""

EX = [46.16, -16.15, 46.51, -15.58]
KAMLOOPS = [-120.597818, 50.581608, -120.037143, 50.804118]
VAN = [-123.303331, 49.011049, -122.106402, 49.391445]
OKANAGAN = [-119.870187, 49.008013, -119.38009, 49.242196]

INSTANCE_ID = "d6a7dc2f-2fbb-4786-a6cf-91a5e10e249a"
CLIENT_ID = "91439487-66bd-4f7a-a6ad-29895c311a51"
CLIENT_SECRET = "U&5::8|HL%_SY&KOObGV&>s|6i&BR_QtdnW.E8]W"

RESOLUTION = 60

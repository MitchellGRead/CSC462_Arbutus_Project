from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import json
import requests

def main():
        # Your client credentials
        client_id = 'f2dc92d4-bb01-4c0c-a727-6324293aff6e'
        client_secret = '1.c!>md*8<g%>17a-J2oiP|m9h:7x#^s!)!6Tj|Z'

        # Create a session
        client = BackendApplicationClient(client_id=client_id)
        oauth = OAuth2Session(client=client)

        # Get token for the session
        token = oauth.fetch_token(token_url='https://services.sentinel-hub.com/oauth/token',
		client_id=client_id, client_secret=client_secret)

	response = requests.post('https://services.sentinel-hub.com/api/v1/process',
	headers={"Authorization" : f"Bearer {token['access_token']}"},
	json={
	"input": {
		"bounds": {
		"bbox": [
			13.822174072265625,
			45.85080395917834,
			14.55963134765625,
			46.29191774991382
		]
		},
		"data": [{
			"type": "sentinel-2-l2a"
		}]
		},
		"evalscript": """
		//VERSION=3

		function setup() {
			return {
				input: ["B02", "B03", "B04"],
				output: {
					bands: 3
				}
			};
	    	}

		function evaluatePixel(sample,scenes,inputMetadata,customData,outputMetadata) {
			return [2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02];
		}
		"""
	})

	print(response)


if __name__ == '__main__':
	main()
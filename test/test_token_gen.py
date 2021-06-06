from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import json

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

	# All requests using this session will have an access token automatically added
	resp = oauth.get("https://services.sentinel-hub.com/oauth/tokeninfo")
	json_data = json.loads(resp.content)
	print(token)
	print(json.dumps(json_data, indent=2))


if __name__ == '__main__':
	main()
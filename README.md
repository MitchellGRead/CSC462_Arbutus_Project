# CSC462_Arbutus_Project

To run the prototype client/server interaction:

1. Navigate to `src/python`, set `export FLASK_APP=server.py` and start the Flask server with `flask run`
2. Ensure the client in `src/python` is pointing to the right host/port that the Flask server has started on. Typically will be `localhost:5000`
3. In `src/python`, run the client with `python3 client.py`
4. The downloaded data will be available in the same directory as the client.

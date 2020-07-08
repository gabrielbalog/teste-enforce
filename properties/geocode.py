import os

import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key=os.environ.get("GOOGLE_MAPS_API_KEY"))
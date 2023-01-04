# IsraelTrainAPI

A Python wrapper for the Israel Train API.

## Installation

To install the package, run:

```bash
pip install israel-train-api

# Usage
To use the package, create an instance of the IsraelTrainAPI class and call its methods:

from israel_train_api import IsraelTrainAPI

api = IsraelTrainAPI()

# Get a list of all station names
station_names = api.get_station_names()
print(station_names)

# Get all routes from a specific source to a specific destination
routes = api.get_routes(source='תל אביב מכבי', destination='נתניה')
print(routes)

# Get all routes from a specific source to a specific destination in the next 60 minutes
next_departures = api.get_next_departures(source='תל אביב מכבי', destination='נתניה')
print(next_departures)

# Get all routes from a specific source to a specific destination on a specific date and time
routes = api.get_routes(source='תל אביב מכבי', destination='נתניה', time='20:00', date='10/01/2022')
print(routes)

# API Reference
## 'IsraelTrainAPI'
The main class for interacting with the API.

__init__(self) -> None
Creates an instance of the IsraelTrainAPI class.

get_station_names(self) -> List[str]
Gets a list of all station names.

get_routes(self, source: str, destination: str, time: Optional[str] = None, date: Optional[str] = None) -> List[Dict[str, Union[str, int]]]
Gets all routes from a specific source to a specific destination.

Parameters
source (str): The name of the source station.
destination (str): The name of the destination station.
time (str, optional): The time of the desired departure (in the format HH:MM). If not provided, returns all routes.
date (str, optional): The date of the desired departure (in the format DD/MM/YYYY). If not provided, defaults to the current date.
Returns
A list of dictionaries, each representing a route. Each dictionary contains the following keys:
departure_time: The departure time (in the format HH:MM).
arrival_time: The arrival time (in the format HH:MM).
duration: The duration of the route (in the format HH:MM).
price: The price of the route.
train_type: The type of train (e.g. "רכבת מהירה

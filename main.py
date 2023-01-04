import requests


class IsraelTrainAPI:
    def __init__(self):
        # Initialize the IsraelRailApi instance
        self.rail_api = israelrailapi.TrainSchedule()

    def get_departures(self, station_code):
        """
        Gets real-time departure information for a given station.

        Parameters:
            - station_code (str): The station code for the station you want to get departure information for.

        Returns:
            - A list of dictionaries, each representing a departure. Each dictionary contains the following keys:
                - 'destination_name': The name of the destination station.
                - 'departure_time': The departure time (in the format HH:MM).
                - 'track': The track number for the departure.
                - 'train_number': The train number for the departure.
                - 'type': The type of train (e.g. "יבנה - רכבת מהירה", "דוד המלך - רכבת רגילה").
        """
        params = {
            "StationCode": station_code
        }

        response = requests.get(self.base_url, params=params)
        data = response.json()

        departures = []
        for train in data['RealTimeDepartures']:
            departure = {
                'destination_name': train['Destination'],
                'departure_time': train['Time'],
                'track': train['Track'],
                'train_number': train['TrainNumber'],
                'type': train['Type']
            }
            departures.append(departure)

        return departures

    def get_station_names(self):
        """
        Gets a list of all train station names.

        Returns:
            - A list of strings, each representing the name of a train station.
        """
        response = requests.get(self.stations_url)
        data = response.json()

        station_names = []
        for station in data['Stations']:
            station_names.append(station['Name'])

        return station_names

    def get_routes(self, source, destination, time=None, date=None):
        """
        Gets all routes from a specific source to a specific destination.

        Parameters:
            - source (str): The name of the source station.
            - destination (str): The name of the destination station.
            - time (str, optional): The time of the desired departure (in the format HH:MM). If not provided, returns all routes.
            - date (str, optional): The date of the desired departure (in the format DD/MM/YYYY). If not provided, defaults to the current date.

        Returns:
            - A list of dictionaries, each representing a route. Each dictionary contains the following keys:
                - 'departure_time': The departure time (in the format HH:MM).
                - 'arrival_time': The arrival time (in the format HH:MM).
                - 'duration': The duration of the route (in the format HH:MM).
                - 'price': The price of the route.
                - 'train_type': The type of train (e.g. "רכבת מהירה", "רכבת רגילה").
        """
        # Query the IsraelRailApi instance for the train routes

        routes = self.rail_api.query(source, destination)

        # Create a list to store the formatted route information
        formatted_routes = []

        # Iterate over the routes and format the information
        for route in routes:
            formatted_route = {
                'departure_time': route.start_time,
                'arrival_time': route.end_time,
                'duration': self._format_duration(route.start_time, route.end_time),
                'price': None,  # The IsraelRailApi class does not provide price information
                'train_type': None  # The IsraelRailApi class does not provide train type information
            }
            formatted_routes.append(formatted_route)

        return formatted_routes

    def _format_duration(self, start_time, end_time):
        """
        Calculates the duration between two times in the format HH:MM.

        Parameters:
            - start_time (str): The start time (in the format HH:MM).
            - end_time (str): The end time (in the format HH:MM).

        Returns:
            - The duration between the two times (in the format HH:MM).
        """
        # Parse the start and end times
        start = datetime.datetime.strptime(start_time, "%d/%m/%Y %H:%M:%S")
        end = datetime.datetime.strptime(end_time, "%d/%m/%Y %H:%M:%S")

        # Calculate the duration and format it as a string
        duration = end - start
        hours, remainder = divmod(duration.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}"

    def get_next_departures(self, source, destination, time=None, date=None):
        """
        Gets all routes from a specific source to a specific destination in the next 60 minutes.

        Parameters:
            - source (str): The name of the source station.
            - destination (str): The name of the destination station.
            - time (str, optional): The current time (in the format HH:MM). If not provided, uses the current time.
            - date (str, optional): The current date (in the format DD/MM/YYYY). If not provided, defaults to the current date.

        Returns:
            - A list of dictionaries, each representing a route. Each dictionary contains the following keys:
                - 'departure_time': The departure time (in the format HH:MM).
                - 'arrival_time': The arrival time (in the format HH:MM).
                - 'duration': The duration of the route (in the format HH:MM).
                - 'price': The price of the route.
                - 'train_type': The type of train (e.g. "רכבת מהירה", "רכבת רגילה").
        """
        if time is None:
            time = datetime.now().strftime("%H:%M")
        if date is None:
            date = datetime.now().strftime("%d/%m/%Y")

        all_routes = self.get_routes(source, destination, date=date)
        next_departures = []
        for route in all_routes:
            departure_time = route['departure_time']
            if self._time_diff(departure_time, time) <= 60:
                next_departures.append(route)

        return next_departures

    def _get_station_code(self, station_name):
        """
        Gets the station code for a given station name.

        Parameters:
            - station_name (str): The name of the station.

        Returns:
            - The station code for the station, or None if the station name is invalid.
        """
        station_names = self.get_station_names()
        if station_name not in station_names:
            return None

        response = requests.get(self.stations_url)
        data = response.json()

        for station in data['Stations']:
            if station['Name'] == station_name:
                return station['Code']

    def _time_diff(self, time1, time2):
        """
        Calculates the difference in minutes between two times.

        Parameters:
            - time1 (str): The first time (in the format HH:MM).
            - time2 (str): The second time (in the format HH:MM).

        Returns:
            - The difference in minutes between the two times.
        """
        fmt = '%H:%M'
        t1 = datetime.strptime(time1, fmt)
        t2 = datetime.strptime(time2, fmt)
        diff = t1 - t2
        return diff.total_seconds() // 60

    def _correct_station_name(self, station_name):
        """
        Attempts to correct a misspelled station name.

        Parameters:
            - station_name (str): The potentially misspelled station name.

        Returns:
            - The corrected station name, or the original name if no correction is found.
        """
        station_names = self.get_station_names()
        candidates = []
        for name in station_names:
            if self._similarity(station_name, name) > 0.8:
                candidates.append(name)
        if len(candidates) == 1:
            return candidates[0]
        return station_name

    def _similarity(self, string1, string2):
        """
        Calculates the similarity between two strings.

        Parameters:
            - string1 (str): The first string.
            - string2 (str): The second string.

        Returns:
            - A float in the range [0, 1], representing the similarity between the two strings.
        """
        string1 = string1.lower()
        string2 = string2.lower()
        common = Counter(string1) & Counter(string2)
        num_common = sum(common.values())
        if num_common == 0:
            return 0
        sum_length = sum(len(string1), len(string2))
        return 2 * num_common / sum_length


import requests
import pandas as pd


class FlightSearch:
    TEQUILA_API_URL = "https://api.tequila.kiwi.com/"
    FROM_AIRPORT = "ZRH"
    CURRENCY = "CHF"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_iata_code(self, city: str) -> str:
        auth_header = {
            "apikey": self.api_key
        }
        params = {
            "term": city
        }
        locations_url = self.TEQUILA_API_URL + "locations/query"
        print(f"Getting IATA code for {city}")
        response = requests.get(
            locations_url, params=params, headers=auth_header)
        response.raise_for_status()
        data = response.json()
        # print(data)
        df = pd.json_normalize(data['locations'])
        filtered_df = df[df['city.name'] == city]
        code = filtered_df['city.code'].iloc[0]
        return code

    def get_cheapest_flight(self, from_date: str,
                            to_date: str, iata_code: str) -> dict | None:
        auth_header = {
            "apikey": self.api_key
        }
        params = {
            "fly_from": self.FROM_AIRPORT,
            "fly_to": iata_code,
            "date_from": from_date,
            "date_to": to_date,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 30,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 3,
            "curr": self.CURRENCY
        }
        locations_url = self.TEQUILA_API_URL + "search"
        print(f"""Getting cheapest flight from
              {self.FROM_AIRPORT} to {iata_code}""")
        response = requests.get(
            locations_url, params=params, headers=auth_header)
        response.raise_for_status()

        try:
            data = response.json()
            df = pd.json_normalize(data['data'])
            stopovers = self.get_via_stations(df)
            cheapest_flight = df[['cityFrom', 'price', 'airlines', 'cityTo',
                                  'dTimeUTC']].iloc[0].to_dict()
            cheapest_flight['stopovers'] = stopovers
        except (IndexError, KeyError):
            print(f"No flights found for {iata_code}.")
            return None
        else:
            cheapest_flight = {
                **cheapest_flight,
                "from_iata": self.FROM_AIRPORT,
                "to_airport_code": iata_code}
            return cheapest_flight

    def get_via_stations(self, flight_data: pd.DataFrame) -> list:
        df_routes = flight_data["route"]
        via_stations = [leg['cityFrom']
                        for route in df_routes for leg in route[:-1]] + [
            route[-1]['cityTo'] for route in df_routes]
        # Find the departure city and the final destination
        departure_city = via_stations[0]
        final_destination = via_stations[-2]

        # Extract the stopover cities
        stopovers = [city for city in via_stations[1:-1]
                     if city != departure_city
                     and city != final_destination]
        print(f"Stopovers: {stopovers}")
        return stopovers

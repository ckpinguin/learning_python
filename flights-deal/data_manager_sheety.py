import requests


class DataManager:
    def __init__(self, sheet_url: str, token: str):
        self.sheet_url = sheet_url
        self.token = token
        # self.flights: dict = self.get_data()
        self.auth_header = {
            "Authorization": f"Bearer {self.token}"
        }

    def get_data(self) -> list[dict]:
        response = requests.get(
            self.sheet_url, headers=self.auth_header)
        response.raise_for_status()
        data: dict = response.json()
        flights: list[dict] = data["flights"]
        return flights

    def get_empty_iata_list(self) -> list[dict]:
        empty_iata_codes = [
            {'city': city_data['city'], 'id': city_data['id']}
            for city_data in self.get_data() if city_data
            ["iataCode"] in ('', None)
        ]
        return empty_iata_codes

    def get_id_for_iata(self, iata: str) -> int:
        sheet_data = self.get_data()
        filtered = [item['id']
                    for item in sheet_data
                    if item.get('iataCode') == iata]
        return filtered[0]

    def get_price_for_id(self, id: int) -> int:
        sheet_data = self.get_data()
        sheet_data

    def put_iata_code(self, id: int, code: str) -> None:
        body = {
            "flight": {
                "iataCode": code
            }
        }
        url = self.sheet_url + f"{id}"
        print(f"Putting iata code into sheet: {body}")
        response = requests.put(
            url, json=body, headers=self.auth_header)
        response.raise_for_status()
        print(response, response.text)

    def put_cheapest_flight(self, id: int, price: int,
                            airlines: list[str], date: str):
        body = {
            "flight": {
                "lowestPrice": price,
                "airlines": " ".join(airlines),
                "date": date
            }
        }
        url = self.sheet_url + f"{id}"
        print(f"Putting flight in sheet: {id} => {body}")
        response = requests.put(
            url, json=body, headers=self.auth_header)
        response.raise_for_status()
        print(response, response.text)

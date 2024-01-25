import gspread
from oauth2client.service_account import ServiceAccountCredentials


class DataManager:

    def __init__(self, sheet_url="Flights Deals", token=""):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            '.credentials.json', scope)
        self.gc = gspread.authorize(credentials)
        # self.gc = gspread.oauth()
        self.sheet = self.gc.open(sheet_url)

        self.sheet_url = sheet_url
        self.worksheet_flights = self.sheet.worksheet('flights')
        self.token = token

    def get_data(self) -> list[dict]:
        flights = self.worksheet_flights.get_all_records()
        # keys = flights[0]
        # flights_dicts = [dict(zip(keys, row)) for row in flights[1:]]
        # return flights_dicts
        return flights

    def get_empty_iata_list(self) -> list[dict]:
        empty_iata_codes = [
            flight for flight in self.get_data() if not flight['IATA Code']]
        return empty_iata_codes

    def get_price_for_id(self, id: int) -> int:
        data = self.get_data()
        row = next((row for row in data if row.get('ID') == f"ID_{id}"))
        price = row.get('Lowest Price')
        return price

    def get_id_for_iata(self, iata: str) -> int:
        data = self.get_data()
        entry = next(
            (entry for entry in data if entry.get("IATA Code") == iata))
        id = int(entry.get('ID').split('_')[1])
        return id

    def get_coords_for_field_by_id(self, field: str, id: int) -> tuple:
        id_cell = self.worksheet_flights.find(f"ID_{id}")
        row = id_cell.row
        field_cell = self.worksheet_flights.find(field)
        col = field_cell.col
        return (row, col)

    def put_iata_code(self, id: int, code: str) -> None:
        row, col = self.get_coords_for_field_by_id("IATA Code", id)

        self.worksheet_flights.update_cell(row, col, code)

    def put_cheapest_flight(self, id: int, price: int,
                            airlines: list[str], date: str,
                            via_cities: list = []):
        print(f"Updating: ID_{id} => {price} {airlines} {date} {via_cities}")
        row_price, col_price = self.get_coords_for_field_by_id(
            "Lowest Price", id)
        self.worksheet_flights.update_cell(row_price, col_price, price)
        row_airlines, col_airlines = self.get_coords_for_field_by_id(
            "Airlines", id)
        self.worksheet_flights.update_cell(
            row_airlines, col_airlines, " ".join(airlines))
        row_date, col_date = self.get_coords_for_field_by_id("Date", id)
        self.worksheet_flights.update_cell(row_date, col_date, date)
        row_via_cities, col_via_cities = self.get_coords_for_field_by_id(
            "Via Cities", id)
        self.worksheet_flights.update_cell(
            row_via_cities, col_via_cities, " ".join(via_cities))

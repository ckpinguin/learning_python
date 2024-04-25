import gspread
from oauth2client.service_account import ServiceAccountCredentials


class DataManager:

    def __init__(self, sheet_name):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            '.credentials.json', scope)
        self.gsession = gspread.authorize(credentials)
        # self.gc = gspread.oauth()
        sheet = self.gsession.open(sheet_name)
        self.worksheet = sheet.worksheet(sheet_name)

    def get_data(self) -> list[dict]:
        data = self.worksheet.get_all_records()
        return data

    def get_coords_for_field_by_id(self, field: str, id: int) -> tuple:
        id_cell = self.worksheet.find(f"ID_{id}")
        row = id_cell.row
        field_cell = self.worksheet.find(field)
        col = field_cell.col
        return (row, col)

    """ def put_iata_code(self, id: int, code: str) -> None:
        row, col = self.get_coords_for_field_by_id("IATA Code", id)

        self.worksheet.update_cell(row, col, code) """

    """ def put_cheapest_flight(self, id: int, price: int,
                            airlines: list[str], date: str,
                            via_cities: list = []):
        print(f"Updating: ID_{id} => {price} {airlines} {date} {via_cities}")
        row_price, col_price = self.get_coords_for_field_by_id(
            "Lowest Price", id)
        self.worksheet.update_cell(row_price, col_price, price)
        row_airlines, col_airlines = self.get_coords_for_field_by_id(
            "Airlines", id)
        self.worksheet.update_cell(
            row_airlines, col_airlines, " ".join(airlines))
        row_date, col_date = self.get_coords_for_field_by_id("Date", id)
        self.worksheet.update_cell(row_date, col_date, date)
        row_via_cities, col_via_cities = self.get_coords_for_field_by_id(
            "Via Cities", id)
        self.worksheet.update_cell(
            row_via_cities, col_via_cities, " ".join(via_cities)) """

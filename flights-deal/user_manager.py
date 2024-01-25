import gspread
from oauth2client.service_account import ServiceAccountCredentials


class UserManager:

    def __init__(self, sheet_url="Flights Deals", token=""):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            '.credentials.json', scope)
        self.gc = gspread.authorize(credentials)
        # self.gc = gspread.oauth()
        self.sheet = self.gc.open(sheet_url)

        self.sheet_url = sheet_url
        self.worksheet_users = self.sheet.worksheet('users')
        self.token = token

    def get_data(self) -> list[dict]:
        flights = self.worksheet_users.get_all_records()
        return flights

    def register_user(self, first_name: str,
                      last_name: str, email: str) -> None:
        new_row_data = [first_name, last_name, email]
        print(f"Registering {new_row_data}")
        self.worksheet_users.append_row(
            [*new_row_data],
            value_input_option='RAW', insert_data_option='INSERT_ROWS')
        return True

    def get_coords_for_field_by_id(self, field: str, id: int) -> tuple:
        id_cell = self.worksheet_users.find(f"ID_{id}")
        row = id_cell.row
        field_cell = self.worksheet_users.find(field)
        col = field_cell.col
        return (row, col)

    def get_all_email_addrs(self) -> list[str]:
        email_column = self.worksheet_users.col_values(
            3)  # Adjust the column index if needed
        # Exclude the header (assuming the first row contains headers)
        email_addresses = email_column[1:]
        return email_addresses

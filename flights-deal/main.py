from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager
import json
import datetime as dt
from user_manager import UserManager

with open('.secret.json') as env_file:
    config_data = json.load(env_file)

sheety_url = config_data["SHEETY_API_URL"] + "flightsFinder/flights/"
api_key_tequila = config_data["API_KEY_TEQUILA"]
email_addr = config_data["RECIPIENT_ADDR"]

flight_search = FlightSearch(api_key_tequila)
notification_manager = NotificationManager()
data_manager = DataManager()
user_manager = UserManager()

sheet_data: list[dict] = data_manager.get_data()
empty_iata_codes: list[dict] = data_manager.get_empty_iata_list()
entry: dict
for entry in empty_iata_codes:
    city = entry.get('City')
    iata_code = flight_search.get_iata_code(city)
    print(iata_code)
    id = int(entry.get('ID').split('_')[1])

    print(id)
    data_manager.put_iata_code(id=id, code=iata_code)

today = dt.datetime.now()
today_formatted = today.strftime("%d/%m/%Y")
six_months_later = today + dt.timedelta(days=6*30)
six_months_later_formatted = six_months_later.strftime("%d/%m/%Y")

destinations = [city_data['IATA Code']
                for city_data in sheet_data if city_data['IATA Code'] != '']


for destination in destinations:
    flight_dict = flight_search.get_cheapest_flight(
        from_date=today_formatted, to_date=six_months_later_formatted,
        iata_code=destination)
    if flight_dict is None:
        print(f"No flights for {destination}")
    else:
        via_cities = flight_dict.get('stopovers')
        stopovers = len(via_cities)
        flight = FlightData(price=flight_dict.get("price"),
                            departure_airport_code=flight_dict.get(
                                "from_iata"),
                            to_airport_code=flight_dict.get("to_airport_code"),
                            to_city=flight_dict.get('cityTo'),
                            departure_city=flight_dict.get("cityFrom"),
                            airlines=flight_dict.get("airlines"),
                            dTimeUTC=flight_dict.get("dTimeUTC"),
                            stop_overs=stopovers,
                            via_cities=via_cities
                            )
        price = flight.price
        date = flight.departure_time
        city = flight.to_city
        via_cities = flight.via_cities
        id = data_manager.get_id_for_iata(destination)
        old_price = data_manager.get_price_for_id(id)
        print(f"old_price: {old_price}")
        print(f"new_price: {price}")
        if price < old_price:
            data_manager.put_cheapest_flight(
                id, price=flight.price, airlines=flight.airlines,
                date=flight.departure_time, via_cities=via_cities)
            addrs = user_manager.get_all_email_addrs()
            notification_manager.send_emails(addrs, old_price=old_price,
                                             new_price=price, city=city,
                                             via_cities=via_cities, date=date)
        else:
            print("Nothing to update...")

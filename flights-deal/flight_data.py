import datetime as dt


class FlightData:
    def __init__(
        self,
        price=0,
        departure_airport_code="",
        to_airport_code="",
        departure_city="",
        to_city="",
        airlines=[],
        dTimeUTC=0,
        stop_overs=0,
        via_cities=[]
    ):
        self.price: float = price
        self.departure_airport_code: str = departure_airport_code
        self.to_airport_code: str = to_airport_code
        self.departure_city: str = departure_city
        self.to_city: str = to_city
        self.airlines: list[str] = airlines
        dt_object = dt.datetime.utcfromtimestamp(dTimeUTC)
        self.departure_time: str = dt_object.strftime("%d/%m/%Y")
        self.stop_overs = stop_overs
        self.via_cities = via_cities

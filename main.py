#This file will need to use the DataManager,FlightSearch,
#FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
import datetime

ORIGIN_CITY_IATA = "LON"

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()


if sheet_data[0]["iataCode"] == "":
    from flight_search import FlightSearch
    flight_search = FlightSearch()
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    print(sheet_data)

    data_manager.destination_data = sheet_data
    data_manager.update_destination_code()

tmr = datetime.datetime.now() + datetime.timedelta(days=1)
in_180_days = datetime.datetime.now() + datetime.timedelta(days=180)

for destination in sheet_data:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tmr,
        to_time=in_180_days,
    )

    if flight is None:
        continue

    if flight.price < destination["lowestPrice"]:
        users = data_manager.get_user_emails()
        emails = [row["email"] for row in users]
        names = [row["firstName"] for row in users]
        message=f"Low price alert! Only £{flight.price} to fly from\
            {flight.origin_city}-{flight.origin_airport}\
            to {flight.destination_city}-{flight.destination_airport},\
            from {flight.out_date} to {flight.return_date}."

        if flight.stop_overs > 0:
            message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."

        notification_manager.send_emails(emails, message)

import requests
from pprint import pprint

sheety_endpoint = "YOUR SHEETY ENDPOINT"
sheety_user_endpoint = "YOUR SHEETY USER SHEET ENDPOINT"
class DataManager:

    def __init__(self):
        self.destination_data = {}
    #This class is responsible for talking to the Google Sheet.
    def get_destination_data(self):
        response = requests.get(url=sheety_endpoint)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_code(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(url=f"{sheety_endpoint}/{city['id']}",
                                    json=new_data)
            print(response.text)

    def get_user_emails(self):
        customers_endpoint = sheety_user_endpoint
        user_response = requests.get(customers_endpoint)
        data = user_response.json()
        self.customer_data = data["users"]
        return self.customer_data



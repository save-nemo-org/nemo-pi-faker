#!/usr/bin/env python3

from json import load, dumps
# import sys
from faker import Faker
from random import uniform, randrange, choices
from string import ascii_letters, digits
import datetime
import pytz
import geonames


class PiData:

    config_data = None
    fake = Faker()

    def __init__(self):

        self.config_data = self.load_config()

    def load_config(self):

        try:
            f = open('config.json',)
            data = load(f)
            f.close()

            return data

        except:
            return "Error reading config"

    def get_timezone(self,lat,lng):
        geonames_client = geonames.GeonamesClient('piData')
        timezone = geonames_client.find_timezone({'lat': lat, 'lng': lng})
        return timezone

    def buoy_info(self):

       # for sensor in self.config_data:
        # print(sensor)

        buoy_data = {
            "serial_number": ''.join(choices(ascii_letters + digits, k=16)),
            "ip_address": self.fake.ipv4(),
            "battery_level": "{:.2f}".format(uniform(0.00, 100.00)),
            "gsm_strength": "-95.4",
            "latitude": "-36.804215",
            "longitude": "174.842076",
            "solar_voltage": "{:.2f}".format(uniform(0, 12.5)),
            "solar_amperage": "{:.2f}".format(uniform(0, 2.5)),
            "measurements": [self.__get_sensor(sensor) for sensor in self.config_data]
        }

        return dumps(buoy_data)

    def __get_sensor(self, sensor_id):

        utc_now = pytz.utc.localize(datetime.datetime.utcnow())

        

        sensor = self.config_data[sensor_id]

        return {

            "sensor": {
                "correction_value": "{:.2f}".format(uniform(0.00, 10.00)),
                "details": {
                    "name": sensor["name"],
                    "unit": sensor["unit"]
                },
                "serial_number": sensor_id,
                "name": sensor["name"]
            },
            "value": self.__get_sensor_data(sensor_id),
            "error_text": "",
            "datetime": utc_now.isoformat()


        }

    def sensor_connected(self, sensor_id):
        return self.config_data[sensor_id]['active']

    def __get_sensor_data(self, sensor_id):

        try:
            sensor = self.config_data[sensor_id]
            sensor_type = sensor["type"]

            if sensor_type == "range":
                sensor_min_range = sensor["data"][0]
                sensor_max_range = sensor["data"][1]

                return randrange(sensor_min_range, sensor_max_range)

            elif sensor_type == "range-dec":
                sensor_min_range = sensor["data"][0]
                sensor_max_range = sensor["data"][1]

                return '{0:.2f}'.format(uniform(sensor_min_range, sensor_max_range))

            elif sensor_type == "geo":
                return self.fake.local_latlng(country_code="AU", coords_only=True)

            else:
                return 0

        except KeyError:
            return "Sensor not found"


def main():

    # sensor_id = sys.argv[1]
    fakeData = PiData()
    print(fakeData.buoy_info())
    # sys.stdout.write(fakeData.get_sensor_data(sensor_id))


main()

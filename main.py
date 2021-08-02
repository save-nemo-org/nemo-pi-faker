#!/usr/bin/env python3

import json
import sys
from faker import Faker
import random


class PiData:

    config_data = None
    fake = Faker()

    def __init__(self):

        self.config_data = self.load_config()

    def load_config(self):

        try:
            f = open('config.json',)
            data = json.load(f)
            f.close()

            return data

        except:
            return "Error reading config"

    def sensor_connected(self, sensor_id):
        return self.config_data[sensor_id]['active']

    def get_sensor_data(self, sensor_id):

        try:
            sensor = self.config_data[sensor_id]
            sensor_type = sensor["type"]

            if sensor_type == "range":
                sensor_min_range = sensor["data"][0]
                sensor_max_range = sensor["data"][1]

                return random.randrange(sensor_min_range, sensor_max_range)

            elif sensor_type == "range-dec":
                sensor_min_range = sensor["data"][0]
                sensor_max_range = sensor["data"][1]

                return '{0:.2f}'.format(random.uniform(sensor_min_range, sensor_max_range))

            elif sensor_type == "geo":
                return self.fake.local_latlng(country_code="AU", coords_only=True)

            else:
                return 0

        except KeyError:
            return "Sensor not found"



def main():

    sensor_id = sys.argv[1]
    fakeData = PiData()
    sys.stdout.write(fakeData.get_sensor_data(sensor_id))


main()
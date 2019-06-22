from .base import Module
import requests
import os


class Weather(Module):
    DESCRIPTION = "Check the weather in everyone's favorite city"
    NH_COORDINATES = {
        "x": 40.8075355,
        "y": -73.9647614
    }

    def response(self, query, message):
        r = requests.get("https://api.weather.gov/points/{x},{y}/forecast".format(x=self.NH_COORDINATES["x"],
                                                                                  y=self.NH_COORDINATES["y"]))
        forecast = r.json()['properties']['periods'][0]['detailedForecast']
        return 'Current weather in Morningside Heights: ' + forecast

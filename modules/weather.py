from .base import Module
import requests
import os


class Weather(Module):
    DESCRIPTION = "Check the weather in everyone's favorite city"
    NH_COORDINATES = {
        "x": 42.273541,
        "y": -83.735226,
    }

    def response(self, query, message):
        r = requests.get("https://api.weather.gov/points/{x},{y}/forecast".format(x=self.NH_COORDINATES["x"],
                                                                                  y=self.NH_COORDINATES["y"]))
        forecast = r.json()['properties']['periods'][0]['detailedForecast']
        return 'Current weather in Ann Arbor: ' + forecast

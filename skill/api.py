# Copyright 2021, Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Call the Open Weather Map One Call API through Selene.

The One Call API provides current weather, 48 hourly forecasts, 7 daily forecasts
and weather alert data all in a single API call.  The endpoint is passed a
latitude and longitude from either the user's configuration or a requested
location.

It also supports returning values in the measurement system (Metric/Imperial)
provided, precluding us from having to do the conversions.

"""
import logging

from neon_utils.hana_utils import request_backend
from ovos_utils import LOG

from .weather import WeatherReport

OPEN_WEATHER_MAP_LANGUAGES = (
    "af",
    "al",
    "ar",
    "bg",
    "ca",
    "cz",
    "da",
    "de",
    "el",
    "en",
    "es",
    "eu",
    "fa",
    "fi",
    "fr",
    "gl",
    "he",
    "hi",
    "hr",
    "hu",
    "id",
    "it",
    "ja",
    "kr",
    "la",
    "lt",
    "mk",
    "nl",
    "no",
    "pl",
    "pt",
    "pt_br",
    "ro",
    "ru",
    "se",
    "sk",
    "sl",
    "sp",
    "sr",
    "sv",
    "th",
    "tr",
    "ua",
    "uk",
    "vi",
    "zh_cn",
    "zh_tw",
    "zu"
)


class OpenWeatherMapApi:
    """Use Open Weather Map's One Call API to retrieve weather information"""

    def __init__(self, lang: str = "en"):
        self.language = lang or "en"

    @property
    def lang(self):
        from ovos_utils.log import log_deprecation
        log_deprecation("`lang` is deprecated, use `language`", "4.0.0")
        return self.language

    def get_current_weather_for_coordinates(
        self, measurement_system: str, latitude: float, longitude: float, lang: str = None
    ) -> dict:
        """Issue an API call and map the return value into a weather report

        Args:
            measurement_system: Metric or Imperial measurement units
            latitude: the geologic latitude of the weather location
            longitude: the geologic longitude of the weather location
            lang: language requested
        """
        LOG.info(f"Getting weather in lang={lang}")
        lang = lang or self.language
        request_data = {"api": "onecall",
                        "lat": latitude, "lon": longitude,
                        "unit": measurement_system, "lang_code": lang}
        forecast = request_backend("proxy/weather", request_data)
        formatted = {"main": forecast["current"], "weather": forecast["current"]["weather"]}
        return formatted

    def get_weather_for_coordinates(
        self, measurement_system: str, latitude: float,
        longitude: float, lang: str, timezone: str
    ) -> WeatherReport:
        """Issue an API call and map the return value into a weather report

        Args:
            measurement_system: Metric or Imperial measurement units
            latitude: the geologic latitude of the weather location
            longitude: the geologic longitude of the weather location
            lang: language requested
            timezone: timezone to use for returned WeatherReport
        """
        LOG.info(f"Getting forecast in lang={lang}")
        lang = lang or self.language
        request_data = {"api": "onecall",
                        "lat": latitude, "lon": longitude,
                        "unit": measurement_system, "lang_code": lang}
        forecast = request_backend("proxy/weather", request_data)
        forecast["timezone"] = timezone
        local_weather = WeatherReport(forecast)

        return local_weather

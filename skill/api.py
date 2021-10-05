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

from neon_utils.authentication_utils import find_neon_owm_key
from neon_utils.service_apis.open_weather_map import get_forecast, get_current_weather

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

    def __init__(self, lang: str = "en", api_key: str = None):
        try:
            self.api_key = api_key or find_neon_owm_key()
        except FileNotFoundError:
            self.api_key = None
        self.language = lang or "en"

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
        lang = lang or self.language
        kwargs = {"api_key": self.api_key, "language": lang} if self.api_key else {"language": lang}
        return get_current_weather(latitude, longitude, measurement_system.lower(), **kwargs)

    def get_weather_for_coordinates(
        self, measurement_system: str, latitude: float, longitude: float, lang: str = None
    ) -> WeatherReport:
        """Issue an API call and map the return value into a weather report

        Args:
            measurement_system: Metric or Imperial measurement units
            latitude: the geologic latitude of the weather location
            longitude: the geologic longitude of the weather location
            lang: language requested
        """
        lang = lang or self.language
        kwargs = {"api_key": self.api_key, "language": lang} if self.api_key else {"language": lang}
        response = get_forecast(latitude, longitude, measurement_system.lower(), **kwargs)
        local_weather = WeatherReport(response)

        return local_weather

    def set_language_parameter(self, language_config: str):
        """
        OWM supports 31 languages, see https://openweathermap.org/current#multi

        Convert Mycroft's language code to OpenWeatherMap's, if missing use english.

        Args:
            language_config: The Mycroft language code.
        """
        special_cases = {"cs": "cz", "ko": "kr", "lv": "la"}
        language_part_one, language_part_two = language_config.split('-')
        if language_config.replace('-', '_') in OPEN_WEATHER_MAP_LANGUAGES:
            self.language = language_config.replace('-', '_')
        elif language_part_one in OPEN_WEATHER_MAP_LANGUAGES:
            self.language = language_part_one
        elif language_part_two in OPEN_WEATHER_MAP_LANGUAGES:
            self.language = language_part_two
        elif language_part_one in special_cases:
            self.language = special_cases[language_part_one]

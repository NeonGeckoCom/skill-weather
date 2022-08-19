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

from neon_api_proxy.client.open_weather_map import get_current_weather, \
    get_forecast

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


def owm_language(lang: str):
    """
    OWM supports 31 languages, see https://openweathermap.org/current#multi

    Convert Mycroft's language code to OpenWeatherMap's, if missing use english.

    Args:
        lang: The Mycroft language code.
    """
    special_cases = {"cs": "cz", "ko": "kr", "lv": "la"}
    lang_primary, lang_subtag = lang.split('-')
    if lang.replace('-', '_') in OPEN_WEATHER_MAP_LANGUAGES:
        return lang.replace('-', '_')
    if lang_primary in OPEN_WEATHER_MAP_LANGUAGES:
        return lang_primary
    if lang_subtag in OPEN_WEATHER_MAP_LANGUAGES:
        return lang_subtag
    if lang_primary in special_cases:
        return special_cases[lang_primary]
    return "en"


class OpenWeatherMapApi:
    """Use Open Weather Map's One Call API to retrieve weather information"""

    def __init__(self, lang: str = "en", api_key: str = None):
        self.api_key = api_key
        self.lang = "en-us"
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
        self, measurement_system: str, latitude: float,
        longitude: float, lang: str
    ) -> WeatherReport:
        """Issue an API call and map the return value into a weather report

        Args:
            measurement_system: Metric or Imperial measurement units
            latitude: the geologic latitude of the weather location
            longitude: the geologic longitude of the weather location
            lang: language requested
        """
        lang = lang or self.language
        if not self.lang == lang:
            self.lang = lang
            # self.set_language_parameter(lang)
        kwargs = {"api_key": self.api_key,
                  "language": owm_language(lang)} if self.api_key else \
            {"language": lang}
        response = get_forecast(latitude, longitude,
                                measurement_system.lower(), **kwargs)
        local_weather = WeatherReport(response)

        return local_weather

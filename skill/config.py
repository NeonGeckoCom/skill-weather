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

from neon_utils.user_utils import get_user_prefs

FAHRENHEIT = "fahrenheit"
CELSIUS = "celsius"
METRIC = "metric"
METERS_PER_SECOND = "meters per second"
MILES_PER_HOUR = "miles per hour"


class WeatherConfig:
    """Build an object representing the configuration values for the weather skill."""

    def __init__(self, user_location_config: dict = None, user_units_config: dict = None, skill_config: dict = None):
        user_units_config = user_units_config or dict()
        self.location_config = user_location_config or \
            get_user_prefs()["location"]
        self.unit_system = user_units_config.get("measure") or \
            get_user_prefs()["units"]["measure"]
        self.settings = skill_config or {}

    @property
    def city(self):
        """The current value of the city name in the device configuration."""
        return self.location_config["city"]

    @property
    def country(self):
        """The current value of the country name in the device configuration."""
        return self.location_config["country"]

    @property
    def latitude(self):
        """The current value of the latitude location configuration"""
        return self.location_config["lat"]

    @property
    def longitude(self):
        """The current value of the longitude location configuration"""
        return self.location_config["lng"]

    @property
    def state(self):
        """The current value of the state name in the device configuration."""
        return self.location_config["state"]

    @property
    def speed_unit(self) -> str:
        """Use the core configuration to determine the unit of speed.

        Returns: (str) 'meters_sec' or 'mph'
        """
        if self.unit_system == METRIC:
            speed_unit = METERS_PER_SECOND
        else:
            speed_unit = MILES_PER_HOUR

        return speed_unit

    @property
    def temperature_unit(self) -> str:
        """Use the core configuration to determine the unit of temperature.

        Returns: "celsius" or "fahrenheit"
        """
        unit_from_settings = self.settings.get("units")
        measurement_system = self.unit_system
        if measurement_system == METRIC:
            temperature_unit = CELSIUS
        else:
            temperature_unit = FAHRENHEIT
        if unit_from_settings is not None and unit_from_settings != "default":
            if unit_from_settings.lower() == FAHRENHEIT:
                temperature_unit = FAHRENHEIT
            elif unit_from_settings.lower() == CELSIUS:
                temperature_unit = CELSIUS

        return temperature_unit

# NEON AI (TM) SOFTWARE, Software Development Kit & Application Framework
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2025 Neongecko.com Inc.
# Contributors: Daniel McKnight, Guy Daniels, Elon Gasper, Richard Leeds,
# Regina Bloomstine, Casimiro Ferreira, Andrii Pernatii, Kirill Hrymailo
# BSD-3 License
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from typing import Literal, List, Dict, Any, Optional
from pydantic import BaseModel, Field, model_validator


class WeatherRequest(BaseModel):
    location: str = Field(description="Location to get weather for")
    unit: Literal["metric", "imperial"] = Field(
        default="metric", description="Unit of measurement for weather data"
    )


class WeatherCondition(BaseModel):
    dt: int = Field(description="timestamp of the forecasted condition")
    temp: float = Field(description="temperature")
    feels_like: float = Field(description="perceived temperature")
    pressure: int = Field(description="atmospheric pressure in hPa")
    humidity: int = Field(description="humidity percentage")
    dew_point: float = Field(description="dew point temperature")
    uvi: float = Field(description="UV index")
    clouds: int = Field(description="cloudiness percentage")
    visibility: Optional[int] = Field(description="visibility in meters")
    wind_speed: float = Field(description="wind speed in requested unit")
    wind_deg: int = Field(description="wind direction in degrees")
    weather_id: int = Field(description="weather condition description")
    condition: str = Field(description="weather condition name")
    description: str = Field(description="weather condition description")
    icon: str = Field(description="weather icon id")
    weather: List[Dict[str, Any]] = Field(
        description="raw weather data from API", deprecated=True
    )

    @model_validator(mode="before")
    @classmethod
    def validate_input(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize weather data into a flat structure"""
        weather_data = data.get("weather", [{}])[0]
        data["weather_id"] = weather_data.get("id", -1)
        data["condition"] = weather_data.get("main", "Unknown")
        data["description"] = weather_data.get("description", "Unknown")
        data["icon"] = weather_data.get("icon", "")
        return data


class DailyWeatherCondition(WeatherCondition):
    summary: str = Field(description="summary of the day's weather")
    visibility = None  # Daily data does not include visibility
    temp: Dict[str, float] = Field(
        description="temperature details for the day"
    )
    feels_like: Dict[str, float] = Field(
        description="perceived temperature details for the day"
    )


class MinutelyWeatherCondition(BaseModel):
    dt: int = Field(description="timestamp of the forecasted condition")
    precipitation: float = Field(description="precipitation in mm/h")


class WeatherAlert(BaseModel):
    event: str = Field(description="Name of the alert event")
    start: int = Field(description="Start timestamp of the alert")
    end: int = Field(description="End timestamp of the alert")
    description: str = Field(description="Detailed description of the alert")


class WeatherResponse(BaseModel):
    current: WeatherCondition = Field(description="Current weather data")
    minutely: List[MinutelyWeatherCondition] = Field(
        description="Minutely weather data"
    )
    hourly: List[WeatherCondition] = Field(description="Hourly weather data")
    daily: List[DailyWeatherCondition] = Field(
        description="Daily weather data"
    )
    alerts: Optional[List[WeatherAlert]] = Field(
        default=None, description="Weather alerts"
    )
    # TODO: Shared with `neon-hana`; implement in `neon_data_models`

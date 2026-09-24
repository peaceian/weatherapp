from django.shortcuts import render
import json
import os
import urllib.parse
import urllib.request

import requests
import urllib3

urllib3.disable_warnings()

API_BASE = "https://opendata.cwa.gov.tw/api/v1/rest/datastore"
USER_KEY = os.environ.get("CWA_API_KEY", "CWA-1871AC9A-A399-42A1-B108-8A365C3FB8BE")
HEADERS = {"User-Agent": "weatherapp/1.0"}


def cwa_get(dataset, params=None):
    query = {"Authorization": USER_KEY}
    if params:
        query.update(params)
    response = requests.get(
        f"{API_BASE}/{dataset}",
        params=query,
        headers=HEADERS,
        verify=False,
        timeout=20,
    )
    response.raise_for_status()
    return response.json()


def _new_locations(payload):
    """Return locations from the new CWA D0047 response schema."""
    return payload.get("records", {}).get("Locations", [])


def _weather_elements(location):
    return {
        element.get("ElementName"): element
        for element in location.get("WeatherElement", [])
        if element.get("ElementName")
    }


def _element_value(time_item):
    values = time_item.get("ElementValue") or []
    if not values:
        return "", ""
    value = values[0] or {}
    if not value:
        return "", ""
    key, result = next(iter(value.items()))
    return result, key


def _element_rows(location, element_name):
    element = _weather_elements(location).get(element_name, {})
    rows = []
    for time_item in element.get("Time", []):
        value, unit = _element_value(time_item)
        rows.append({
            "startTime": time_item.get("StartTime", ""),
            "endTime": time_item.get("EndTime", ""),
            "value": value,
            "unit": unit,
        })
    return rows


def wr8(request):
    payload = cwa_get("F-C0032-001")
    locations = payload.get("records", {}).get("location", [])
    rows = []
    for location in locations:
        elements = {
            item.get("elementName"): item
            for item in location.get("weatherElement", [])
        }
        def value(name):
            times = elements.get(name, {}).get("time", [])
            return (times[0].get("parameter", {}) or {}).get("parameterName", "") if times else ""
        start = next((item.get("time", [{}])[0].get("startTime", "") for item in elements.values() if item.get("time")), "")
        rows.append((location.get("locationName", ""), value("Wx"), value("MaxT"), value("MinT"), value("CI"), value("PoP"), start))
    return render(request, "weatherlist.html", {"all": rows})


def searchcity(request):
    data = {}
    if request.method == "POST":
        city = request.POST.get("locationName", "")
        payload = cwa_get("F-C0032-001", {"locationName": city})
        locations = payload.get("records", {}).get("location", [])
        if locations:
            location = locations[0]
            elements = {
                item.get("elementName"): item
                for item in location.get("weatherElement", [])
            }
            def value(name):
                times = elements.get(name, {}).get("time", [])
                return (times[0].get("parameter", {}) or {}).get("parameterName", "") if times else ""
            data = {
                "locationName": location.get("locationName", ""),
                "wr8": value("Wx"), "maxt8": value("MaxT"),
                "mint8": value("MinT"), "ci8": value("CI"), "pop8": value("PoP"),
                "starttime": next((item.get("time", [{}])[0].get("startTime", "") for item in elements.values() if item.get("time")), ""),
            }
    return render(request, "form.html", data)


def oneweek(request):
    context = {"all": []}
    if request.method == "POST":
        city = request.POST.get("locationName", "")
        requested_element = request.POST.get("element", "")
        payload = cwa_get("F-D0047-091", {"locationName": city})
        locations_groups = _new_locations(payload)

        # The new response uses Locations/Location/WeatherElement/Time/ElementValue.
        # Select the requested town and return every forecast period for that element.
        location = next(
            (item for group in locations_groups for item in group.get("Location", [])
             if item.get("LocationName") == city),
            next((item for group in locations_groups for item in group.get("Location", [])), None),
        )
        if location:
            aliases = {
                "MinT": "最低溫度", "MaxT": "最高溫度", "PoP12h": "12小時降雨機率",
                "T": "平均溫度", "Wx": "天氣現象", "WeatherDescription": "天氣預報綜合描述",
            }
            selected = aliases.get(requested_element, requested_element) or "平均溫度"
            element = _weather_elements(location).get(selected)
            if element is None:
                element = next(iter(_weather_elements(location).values()), {})
            rows = _element_rows(location, element.get("ElementName", ""))
            description = element.get("ElementName", "")
            dataset_description = next((g.get("DatasetDescription", "") for g in locations_groups), "")
            context["all"] = [
                (dataset_description, location.get("LocationName", ""), location.get("Geocode", ""),
                 location.get("Latitude", ""), location.get("Longitude", ""), description,
                 row["startTime"], row["endTime"], row["value"], row["unit"])
                for row in rows
            ]
    return render(request, "oneweek.html", context)


def realtimeweather(request):
    stations = cwa_get("O-A0001-001").get("records", {}).get("Station", [])
    all_rows = []
    for station in stations:
        geo = station.get("GeoInfo", {})
        coords = geo.get("Coordinates", [{}])
        coord = coords[0] if coords else {}
        weather = station.get("WeatherElement", {})
        all_rows.append((coord.get("StationLatitude", ""), coord.get("StationLongitude", ""), station.get("StationName", ""), station.get("StationId", ""), station.get("ObsTime", {}).get("DateTime", ""), geo.get("StationAltitude", ""), weather.get("WindDirection", ""), weather.get("WindSpeed", ""), weather.get("AirTemperature", ""), weather.get("RelativeHumidity", ""), weather.get("AirPressure", ""), weather.get("Weather", ""), geo.get("CountyName", ""), geo.get("TownName", "")))
    return render(request, "realtimeweather.html", {"all": all_rows})


def detailone(request):
    data = {}
    if request.method == "POST":
        station = request.POST.get("town", "")
        payload = cwa_get("O-A0001-001", {"StationName": station})
        stations = payload.get("records", {}).get("Station", [])
        if stations:
            item = stations[0]
            geo = item.get("GeoInfo", {})
            weather = item.get("WeatherElement", {})
            data = {"StationName": item.get("StationName", ""), "StationId": item.get("StationId", ""), "obsTime": item.get("ObsTime", {}).get("DateTime", ""), "lat": geo.get("Coordinates", [{}])[0].get("StationLatitude", ""), "lon": geo.get("Coordinates", [{}])[0].get("StationLongitude", ""), "Altitude": geo.get("StationAltitude", ""), "CITY": geo.get("CountyName", ""), "TOWN": geo.get("TownName", ""), "WEATHER": weather.get("Weather", ""), "WDIR": weather.get("WindDirection", ""), "WDSD": weather.get("WindSpeed", ""), "TEMP": weather.get("AirTemperature", ""), "HUMD": weather.get("RelativeHumidity", ""), "PRES": weather.get("AirPressure", "")}
    return render(request, "detailone.html", data)


def cityweek(request):
    return render(request, "cityweek.html", {})


def hello(request):
    return render(request, "homepage.html", {})

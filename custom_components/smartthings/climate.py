"""Support for climate devices through the SmartThings cloud API."""

from homeassistant.components.smartthings import climate


class SmartThingsThermostat(climate.SmartThingsThermostat):
    pass


class SmartThingsAirConditioner(climate.SmartThingsAirConditioner):
    pass

for i in climate.__all__:
    setattr(SmartThingsThermostat, i, getattr(climate, i))
    setattr(SmartThingsAirConditioner, i, getattr(climate, i))
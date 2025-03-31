"""Support for climate devices through the SmartThings cloud API."""

from homeassistant.components.smartthings import climate


class SmartThingsThermostat(climate.SmartThingsThermostat):
    """Representation of a SmartThings thermostat."""


class SmartThingsAirConditioner(climate.SmartThingsAirConditioner):
    """Representation of a SmartThings air conditioner."""

# for i in climate.__all__:
#     setattr(SmartThingsThermostat, i, getattr(climate, i))
#     setattr(SmartThingsAirConditioner, i, getattr(climate, i))
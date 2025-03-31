"""Support for sensors through the SmartThings cloud API."""

from homeassistant.components.smartthings import sensor


class SmartThingsSensor(sensor.SmartThingsSensor):
    print("-------------------------")
    print("TEST TEST TEST")
    print("-------------------------")
    """Representation of a SmartThings sensor."""

# for i in sensor.__all__:
#     setattr(SmartThingsSensor, i, getattr(sensor, i))
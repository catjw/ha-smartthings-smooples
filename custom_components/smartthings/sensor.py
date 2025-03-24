"""Support for sensors through the SmartThings cloud API."""

from homeassistant.components.smartthings import sensor


class SmartThingsSensor(sensor.SmartThingsSensor):
    pass

for i in sensor.__all__:
    setattr(SmartThingsSensor, i, getattr(sensor, i))
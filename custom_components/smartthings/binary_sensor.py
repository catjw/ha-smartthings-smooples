"""Support for binary sensors through the SmartThings cloud API."""

from homeassistant.components.smartthings import binary_sensor

class SmartThingsBinarySensor(binary_sensor.SmartThingsBinarySensor):
    """Representation of a SmartThings binary sensor."""


# for i in binary_sensor.__all__:
#     setattr(SmartThingsBinarySensor, i, getattr(binary_sensor, i))
"""Support for lights through the SmartThings cloud API."""

from homeassistant.components.smartthings import light


class SmartThingsLight(light.SmartThingsLight):
    pass

for i in light.__all__:
    setattr(SmartThingsLight, i, getattr(light, i))
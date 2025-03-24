"""Support for fans through the SmartThings cloud API."""

from homeassistant.components.smartthings import fan


class SmartThingsFan(fan.SmartThingsFan):
    pass

for i in fan.__all__:
    setattr(SmartThingsFan, i, getattr(fan, i))
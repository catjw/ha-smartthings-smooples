"""Support for switches through the SmartThings cloud API."""

from homeassistant.components.smartthings import switch


class SmartThingsSwitch(switch.SmartThingsSwitch):
    pass

for i in switch.__all__:
    setattr(SmartThingsSwitch, i, getattr(switch, i))
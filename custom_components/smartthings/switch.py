"""Support for switches through the SmartThings cloud API."""

from homeassistant.components.smartthings import switch


class SmartThingsSwitch(switch.SmartThingsSwitch):
    """Representation of a SmartThings switch."""


# for i in switch.__all__:
#     setattr(SmartThingsSwitch, i, getattr(switch, i))
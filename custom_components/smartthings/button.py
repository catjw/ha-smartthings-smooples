"""Support for button entities through the SmartThings cloud API."""

from homeassistant.components.smartthings import button


class SmartThingsButton(button.SmartThingsButton):
    """Representation of a SmartThings button."""


# for i in button.__all__:
#     setattr(SmartThingsButton, i, getattr(button, i))
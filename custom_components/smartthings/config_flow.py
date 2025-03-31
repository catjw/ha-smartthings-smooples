"""Config flow to configure SmartThings."""

from homeassistant.components.smartthings import config_flow
from homeassistant.components import smartthings

class SmartThingsConfigFlow(config_flow.SmartThingsConfigFlow):
    """Handle a config flow for SmartThings."""

# for i in config_flow.__all__:
#     setattr(SmartThingsConfigFlow, i, getattr(config_flow, i))
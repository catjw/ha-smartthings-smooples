"""Config flow to configure SmartThings."""

from homeassistant.components.smartthings import config_flow

class SmartThingsConfigFlow(config_flow.SmartThingsConfigFlow):
    pass

for i in config_flow.__all__:
    setattr(SmartThingsConfigFlow, i, getattr(config_flow, i))
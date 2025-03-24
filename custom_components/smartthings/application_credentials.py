"""Application credentials platform for SmartThings."""

from homeassistant.components.smartthings import application_credentials

class SmartThingsOAuth2Implementation(application_credentials.SmartThingsOAuth2Implementation):
    pass

for i in application_credentials.__all__:
    setattr(SmartThingsOAuth2Implementation, i, getattr(application_credentials, i))
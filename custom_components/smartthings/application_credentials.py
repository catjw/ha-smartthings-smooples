"""Application credentials platform for SmartThings."""

from homeassistant.components.smartthings import application_credentials

async def async_get_auth_implementation(
    hass, auth_domain, credential
):
    """Return auth implementation."""
    return application_credentials.async_get_auth_implementation(hass, auth_domain, credential)

# for i in application_credentials.__all__:
#     setattr(SmartThingsOAuth2Implementation, i, getattr(application_credentials, i))
"""Application credentials platform for SmartThings."""

from homeassistant.components.application_credentials import (
    ClientCredential,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.config_entry_oauth2_flow import AbstractOAuth2Implementation

from homeassistant.components.smartthings import application_credentials


async def async_get_auth_implementation(
    hass: HomeAssistant, auth_domain: str, credential: ClientCredential
) -> AbstractOAuth2Implementation:
    """Return auth implementation."""
    return await application_credentials.async_get_auth_implementation(
        hass,
        auth_domain,
        credential,
    )

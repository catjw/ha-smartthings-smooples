"""Application credentials platform for SmartThings."""

from json import JSONDecodeError
import logging
from typing import cast

from aiohttp import BasicAuth, ClientError

from homeassistant.components.application_credentials import (
    AuthImplementation,
    AuthorizationServer,
    ClientCredential,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.config_entry_oauth2_flow import AbstractOAuth2Implementation

from homeassistant.components.smartthings.const import DOMAIN

from homeassistant.components.smartthings import application_credentials

_LOGGER = logging.getLogger(__name__)


async def async_get_auth_implementation(
    hass: HomeAssistant, auth_domain: str, credential: ClientCredential
) -> AbstractOAuth2Implementation:
    """Return auth implementation."""
    return application_credentials.SmartThingsOAuth2Implementation(
        hass,
        DOMAIN,
        credential,
        authorization_server=AuthorizationServer(
            authorize_url="https://api.smartthings.com/oauth/authorize",
            token_url="https://auth-global.api.smartthings.com/oauth/token",
        ),
    )

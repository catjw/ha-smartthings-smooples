"""Config flow to configure SmartThings."""

from collections.abc import Mapping
import logging
from typing import Any

from pysmartthings import SmartThings

from homeassistant.config_entries import SOURCE_REAUTH, ConfigFlowResult
from homeassistant.const import CONF_ACCESS_TOKEN, CONF_TOKEN
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.config_entry_oauth2_flow import AbstractOAuth2FlowHandler

from homeassistant.components.smartthings.const import CONF_LOCATION_ID, DOMAIN, OLD_DATA, REQUESTED_SCOPES, SCOPES
from homeassistant.components.smartthings import config_flow

_LOGGER = logging.getLogger(__name__)


class SmartThingsOAuth2FlowHandler(config_flow.SmartThingsConfigFlow):
    """Handle configuration of SmartThings integrations."""

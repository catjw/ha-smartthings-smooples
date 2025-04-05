"""Tests for the SmartThings component init module."""

from unittest.mock import AsyncMock, patch

from aiohttp import ClientResponseError, RequestInfo
from pysmartthings import (
    Attribute,
    Capability,
    DeviceResponse,
    DeviceStatus,
    Lifecycle,
    SmartThingsSinkError,
    Subscription,
)
import pytest
from syrupy import SnapshotAssertion

from homeassistant.components.binary_sensor import DOMAIN as BINARY_SENSOR_DOMAIN
from homeassistant.components.climate import DOMAIN as CLIMATE_DOMAIN, HVACMode
from homeassistant.components.cover import DOMAIN as COVER_DOMAIN
from homeassistant.components.fan import DOMAIN as FAN_DOMAIN
from homeassistant.components.light import DOMAIN as LIGHT_DOMAIN
from homeassistant.components.lock import DOMAIN as LOCK_DOMAIN
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.components.smartthings import EVENT_BUTTON
from homeassistant.components.smartthings.const import (
    CONF_INSTALLED_APP_ID,
    CONF_LOCATION_ID,
    CONF_SUBSCRIPTION_ID,
    DOMAIN,
    SCOPES,
)
from homeassistant.components.switch import DOMAIN as SWITCH_DOMAIN
from homeassistant.config_entries import ConfigEntryState
from homeassistant.const import EVENT_HOMEASSISTANT_STOP
from homeassistant.core import Event, HomeAssistant
from homeassistant.helpers import device_registry as dr, entity_registry as er

from . import setup_integration, trigger_update

from pytest_homeassistant_custom_component.common import MockConfigEntry, load_fixture


async def test_devices(
    hass: HomeAssistant,
    snapshot: SnapshotAssertion,
    devices: AsyncMock,
    mock_config_entry: MockConfigEntry,
    device_registry: dr.DeviceRegistry,
) -> None:
    """Test all entities."""
    await setup_integration(hass, mock_config_entry)

    device_id = devices.get_devices.return_value[0].device_id

    device = device_registry.async_get_device({(DOMAIN, device_id)})

    assert device is not None
    assert device == snapshot
    

@pytest.mark.parametrize("device_fixture", ["button"])
async def test_button_event(
    hass: HomeAssistant,
    devices: AsyncMock,
    mock_config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test button event."""
    await setup_integration(hass, mock_config_entry)
    events = []

    def capture_event(event: Event) -> None:
        events.append(event)

    hass.bus.async_listen_once(EVENT_BUTTON, capture_event)

    await trigger_update(
        hass,
        devices,
        "c4bdd19f-85d1-4d58-8f9c-e75ac3cf113b",
        Capability.BUTTON,
        Attribute.BUTTON,
        "pushed",
    )

    assert len(events) == 1
    assert events[0] == snapshot


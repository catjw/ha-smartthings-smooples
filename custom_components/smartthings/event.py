"""Support for events through the SmartThings cloud API."""

from __future__ import annotations

from typing import cast

from pysmartthings import Attribute, Capability, Component, DeviceEvent, SmartThings

from homeassistant.components.event import EventDeviceClass, EventEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from homeassistant.components.smartthings import FullDevice, SmartThingsConfigEntry, event
from homeassistant.components.smartthings.entity import SmartThingsEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SmartThingsConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add events for a config entry."""
    await event.async_setup_entry(hass, entry, async_add_entities)

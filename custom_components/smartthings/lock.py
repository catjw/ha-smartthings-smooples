"""Support for locks through the SmartThings cloud API."""

from __future__ import annotations

from typing import Any

from pysmartthings import Attribute, Capability, Command

from homeassistant.components.lock import LockEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from homeassistant.components.smartthings import SmartThingsConfigEntry, lock
from homeassistant.components.smartthings.const import MAIN
from homeassistant.components.smartthings.entity import SmartThingsEntity

ST_STATE_LOCKED = "locked"
ST_LOCK_ATTR_MAP = {
    "codeId": "code_id",
    "codeName": "code_name",
    "lockName": "lock_name",
    "method": "method",
    "timeout": "timeout",
    "usedCode": "used_code",
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SmartThingsConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add locks for a config entry."""
    await lock.async_setup_entry(hass, entry, async_add_entities)
    
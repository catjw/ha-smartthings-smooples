"""Support for media players through the SmartThings cloud API."""

from __future__ import annotations

from typing import Any

from pysmartthings import Attribute, Capability, Category, Command, SmartThings

from homeassistant.components.media_player import (
    MediaPlayerDeviceClass,
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
    RepeatMode,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from homeassistant.components.smartthings import FullDevice, SmartThingsConfigEntry, media_player
from homeassistant.components.smartthings.const import MAIN
from homeassistant.components.smartthings.entity import SmartThingsEntity

MEDIA_PLAYER_CAPABILITIES = (
    Capability.AUDIO_MUTE,
    Capability.AUDIO_VOLUME,
    Capability.MEDIA_PLAYBACK,
)

CONTROLLABLE_SOURCES = ["bluetooth", "wifi"]

DEVICE_CLASS_MAP: dict[Category | str, MediaPlayerDeviceClass] = {
    Category.NETWORK_AUDIO: MediaPlayerDeviceClass.SPEAKER,
    Category.SPEAKER: MediaPlayerDeviceClass.SPEAKER,
    Category.TELEVISION: MediaPlayerDeviceClass.TV,
    Category.RECEIVER: MediaPlayerDeviceClass.RECEIVER,
}

VALUE_TO_STATE = {
    "buffering": MediaPlayerState.BUFFERING,
    "paused": MediaPlayerState.PAUSED,
    "playing": MediaPlayerState.PLAYING,
    "stopped": MediaPlayerState.IDLE,
    "fast forwarding": MediaPlayerState.BUFFERING,
    "rewinding": MediaPlayerState.BUFFERING,
}

REPEAT_MODE_TO_HA = {
    "all": RepeatMode.ALL,
    "one": RepeatMode.ONE,
    "off": RepeatMode.OFF,
}

HA_REPEAT_MODE_TO_SMARTTHINGS = {v: k for k, v in REPEAT_MODE_TO_HA.items()}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SmartThingsConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add media players for a config entry."""
    await media_player.async_setup_entry(hass, entry, async_add_entities)

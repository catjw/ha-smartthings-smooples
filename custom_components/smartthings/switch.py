"""Support for switches through the SmartThings cloud API."""

import asyncio
import logging

from dataclasses import dataclass
from typing import Any

from pysmartthings import Attribute, Capability, Command, SmartThings

from homeassistant.core import HomeAssistant
from homeassistant.const import STATE_OFF, STATE_ON
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from homeassistant.components.smartthings.const import INVALID_SWITCH_CATEGORIES, MAIN
from homeassistant.components.smartthings.entity import SmartThingsEntity
from homeassistant.components.smartthings.util import deprecate_entity

from homeassistant.components.smartthings import switch, FullDevice

from . import SmartThingsConfigEntry


_LOGGER = logging.getLogger(__name__)


@dataclass
class SmartThingsCustomSwitch:
    """SmartThings custom switch."""
    attribute: Attribute
    command: str
    translation: str
    on_value: str | int
    off_value: str | int
    icon: str = None


CUSTOM_CAPABILITY_TO_SWITCH = {
    Capability.CUSTOM_SPI_MODE: SmartThingsCustomSwitch(
        attribute=Attribute.SPI_MODE,
        command=Command.SET_SPI_MODE,
        translation="spi_mode",
        on_value="on",
        off_value="off",
    ),
    Capability.CUSTOM_AUTO_CLEANING_MODE: SmartThingsCustomSwitch(
        attribute=Attribute.AUTO_CLEANING_MODE,
        command=Command.SET_AUTO_CLEANING_MODE,
        translation="auto_cleaning_mode",
        on_value="on",
        off_value="off",
        icon="mdi:shimmer",
    ),
    Capability.AUDIO_VOLUME: SmartThingsCustomSwitch(
        attribute=Attribute.VOLUME,
        command=Command.SET_VOLUME,
        translation="volume",
        on_value=100,
        off_value=0,
        icon="mdi:volume-high",
    )
}


@dataclass
class SmartThingsExecuteCommands:
    """SmartThings execute commands."""
    name: str
    page: str
    section: str
    on: str
    off: str

    @property
    def set_off(self) -> list[str, dict[str, list[str]]]:
        """Set off command."""
        return [self.page, {self.section: [self.off]}]
    
    @property
    def set_on(self) -> list[str, dict[str, list[str]]]:
        """Set on command."""
        return [self.page, {self.section: [self.on]}]
    

async def async_setup_entry(
    hass: HomeAssistant,
    entry: SmartThingsConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add switches for a config entry."""
    await switch.async_setup_entry(hass, entry, async_add_entities)
    entry_data = entry.runtime_data
    entities: list[SmartThingsEntity] = []
    for device in entry_data.devices.values():
        media_player = all(
            capability in device.status[MAIN]
            for capability in switch.MEDIA_PLAYER_CAPABILITIES
        )
        appliance = (
            device.device.components[MAIN].manufacturer_category
            in INVALID_SWITCH_CATEGORIES
        )
        if (
            device.device.type == "OCF"
            and not media_player
            and not appliance
            and device.status[MAIN][Capability.OCF][Attribute.MANUFACTURER_NAME].value == "Samsung Electronics"
        ):
            for capability in CUSTOM_CAPABILITY_TO_SWITCH:
                if capability in device.status[MAIN]:
                    entities.append(
                        switch.SmartThingsCommandSwitch(
                            entry_data.client,
                            device,
                            switch.SmartThingsCommandSwitchEntityDescription(
                                key=capability,
                                translation_key=CUSTOM_CAPABILITY_TO_SWITCH[capability].translation,
                                status_attribute=CUSTOM_CAPABILITY_TO_SWITCH[capability].attribute,
                                command=CUSTOM_CAPABILITY_TO_SWITCH[capability].command,
                                icon=CUSTOM_CAPABILITY_TO_SWITCH[capability].icon,
                            ),
                            capability
                        )
                    )
            model = device.status[MAIN][Capability.OCF][Attribute.MODEL_NUMBER].value.split("|")[0]
            if (
                Capability.EXECUTE
                and "Air Conditioner" in device.device.device_type_name
                and "airconditioner" in device.device.ocf.device_type
                and model not in (
                    "SAC_SLIM1WAY",
                    "SAC_BIG_SLIM1WAY",
                    "MIM-H04EN",
                )
            ):
                entities.append(
                    SamsungOcfSwitch(
                        client=entry_data.client,
                        device=device,
                        entity_description=switch.SmartThingsCommandSwitchEntityDescription(
                            key=Capability.EXECUTE,
                            translation_key="light",
                            status_attribute=Attribute.DATA,
                            command=Command.EXECUTE,
                            icon="mdi:lightbulb",
                        ),
                        capability=Capability.EXECUTE,
                        commands=SmartThingsExecuteCommands(
                            'Light',
                            'mode/vs/0', 
                            'x.com.samsung.da.options',
                            'Light_Off',
                            'Light_On',
                        ),
                    )
                )
    async_add_entities(entities)


class SamsungOcfSwitch(switch.SmartThingsCommandSwitch, SmartThingsExecuteCommands):
    """Representation of a Samsung OCF switch."""

    entity_description: switch.SmartThingsCommandSwitchEntityDescription
    commands: SmartThingsExecuteCommands

    def __init__(
        self,
        client: SmartThings,
        device: FullDevice,
        entity_description: switch.SmartThingsCommandSwitchEntityDescription,
        capability: Capability,
        commands: SmartThingsExecuteCommands,
        component: str = MAIN,
    ) -> None:
        """Initialize the switch."""
        super().__init__(client, device, entity_description, capability, component)
        self.commands = commands
    
    def get_attribute_data(self, capability: Capability, attribute: Attribute) -> Any:
        """Get the value of a device attribute."""
        return self._internal_state[capability][attribute].data
    
    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        return self._attr_is_on
    
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        if self._attr_is_on in [None, True]:
            await self.execute_device_command(
                self.switch_capability,
                self.entity_description.command,
                self.commands.set_off
            )
            self._attr_is_on = False

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        if self._attr_is_on in [None, False]:
            await self.execute_device_command(
                self.switch_capability,
                self.entity_description.command,
                self.commands.set_on
            )
            self._attr_is_on = True
"""Support for switches through the SmartThings cloud API."""

from __future__ import annotations

from collections import namedtuple
from collections.abc import Sequence

import asyncio
import logging
from typing import Any

from pysmartthings import Attribute, Capability, Command, SmartThings

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import FullDevice, SmartThingsConfigEntry
from .const import MAIN
from .entity import SmartThingsEntity

_LOGGER = logging.getLogger(__name__)

Map = namedtuple(
    "map",
    "attribute on_command off_command on_value off_value name icon extra_state_attributes",
)

CAPABILITIES = (
    Capability.SWITCH_LEVEL,
    Capability.COLOR_CONTROL,
    Capability.COLOR_TEMPERATURE,
    Capability.FAN_SPEED,
)

AC_CAPABILITIES = (
    Capability.AIR_CONDITIONER_MODE,
    Capability.AIR_CONDITIONER_FAN_MODE,
    Capability.TEMPERATURE_MEASUREMENT,
    Capability.THERMOSTAT_COOLING_SETPOINT,
)

CUSTOM_CAPABILITIES = (
    Capability.CUSTOM_AUTO_CLEANING_MODE,
    Capability.CUSTOM_SPI_MODE,
)

CAPABILITY_TO_SWITCH = {
    Capability.SWITCH: [
        Map(
            Attribute.SWITCH,
            "switch_on",
            "switch_off",
            "on",
            "off",
            "Switch",
            None,
            None,
        )
    ],
    Capability.CUSTOM_SPI_MODE: [
        Map(
            "spiMode",
            "setSpiMode",
            "setSpiMode",
            "on",
            "off",
            "SPI Mode",
            None,
            None,
        )
    ],
    Capability.CUSTOM_AUTO_CLEANING_MODE: [
        Map(
            "autoCleaningMode",
            "setAutoCleaningMode",
            "setAutoCleaningMode",
            "on",
            "off",
            "Auto Cleaning Mode",
            "mdi:shimmer",
            None,
        )
    ],
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SmartThingsConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add switches for a config entry."""
    entry_data = entry.runtime_data
    async_add_entities(
        SmartThingsSwitch(
            entry_data.client, device, entry_data.rooms, 
            capabilities={Capability.SWITCH},
            attribute=CAPABILITY_TO_SWITCH[Capability.SWITCH][0].attribute,
            on_command=CAPABILITY_TO_SWITCH[Capability.SWITCH][0].on_command,
            off_command=CAPABILITY_TO_SWITCH[Capability.SWITCH][0].off_command,
            on_value=CAPABILITY_TO_SWITCH[Capability.SWITCH][0].on_value,
            off_value=CAPABILITY_TO_SWITCH[Capability.SWITCH][0].off_value,
            name=CAPABILITY_TO_SWITCH[Capability.SWITCH][0].name,
            icon=CAPABILITY_TO_SWITCH[Capability.SWITCH][0].icon,
            extra_state_attributes=CAPABILITY_TO_SWITCH[Capability.SWITCH][0].extra_state_attributes,
        )
        for device in entry_data.devices.values()
        if Capability.SWITCH in device.status[MAIN]
        and not any(capability in device.status[MAIN] for capability in CAPABILITIES)
        and not all(capability in device.status[MAIN] for capability in AC_CAPABILITIES)
    )
    _LOGGER.error('---------------------------------------------------')
    custom_switches = []
    for device in entry_data.devices.values():
        for capability in CUSTOM_CAPABILITIES:
            if capability in device.status[MAIN]:
                _LOGGER.error(CAPABILITY_TO_SWITCH[capability])
                custom_switches.extend(
                    [SmartThingsCustomSwitch(
                        entry_data.client, device, entry_data.rooms,
                        capabilities={capability},
                        attribute=CAPABILITY_TO_SWITCH[capability][0].attribute,
                        on_command=CAPABILITY_TO_SWITCH[capability][0].on_command,
                        off_command=CAPABILITY_TO_SWITCH[capability][0].off_command,
                        on_value=CAPABILITY_TO_SWITCH[capability][0].on_value,
                        off_value=CAPABILITY_TO_SWITCH[capability][0].off_value,
                        name=CAPABILITY_TO_SWITCH[capability][0].name,
                        icon=CAPABILITY_TO_SWITCH[capability][0].icon
                    )]
                )
        if device.status[MAIN].get(Capability.OCF,{}).get(Attribute.MANUFACTURER_NAME) == "Samsung Electronics":
            custom_switches.extend([
                SamsungOfcLightSwitch(
                    entry_data.client, device, entry_data.rooms, {Capability.SWITCH}
                )
            ])
    async_add_entities(custom_switches)


class SmartThingsSwitch(SmartThingsEntity, SwitchEntity):
    """Define a SmartThings switch."""

    _attr_name = None
    
    def __init__(
        self,
        client: SmartThings,
        device: FullDevice,
        rooms: dict[str, str],
        capabilities: set[Capability],
        attribute: str,
        on_command: str,
        off_command: str,
        on_value: str | int | None,
        off_value: str | int | None,
        name: str,
        icon: str | None,
        extra_state_attributes: str | None,
    ) -> None:
        """Init the class."""
        super().__init__(
            client=client,
            device=device,
            rooms=rooms,
            capabilities=capabilities
        )
        self._attribute = attribute
        self._on_command = on_command
        self._off_command = off_command
        self._on_value = on_value
        self._off_value = off_value
        self._name = name
        self._icon = icon
        self._extra_state_attributes = extra_state_attributes

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self.execute_device_command(
            Capability.SWITCH,
            Command.OFF,
        )
        # State is set optimistically in the command above, therefore update
        # the entity state ahead of receiving the confirming push updates
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self.execute_device_command(
            Capability.SWITCH,
            Command.ON,
        )
        # State is set optimistically in the command above, therefore update
        # the entity state ahead of receiving the confirming push updates
        self.async_write_ha_state()

    @property
    def is_on(self) -> bool:
        """Return true if light is on."""
        return self.get_attribute_value(Capability.SWITCH, Attribute.SWITCH) == "on"

    @property
    def icon(self) -> str | None:
        return self._icon


class SmartThingsCustomSwitch(SmartThingsEntity, SwitchEntity):
    """Define a SmartThings custom switch."""

    def __init__(
        self,
        client: SmartThings,
        device: FullDevice,
        rooms: dict[str, str],
        capabilities: set[Capability],
        attribute: str,
        on_command: str,
        off_command: str,
        on_value: str | int | None,
        off_value: str | int | None,
        name: str,
        icon: str | None,
    ) -> None:
        """Init the class."""
        super().__init__(
            client=client,
            device=device,
            rooms=rooms,
            capabilities=capabilities
        )
        self._capability = capabilities.pop()
        self._attribute = attribute
        self._on_command = on_command
        self._off_command = off_command
        self._on_value = on_value
        self._off_value = off_value
        self._name = name
        self._icon = icon
        _LOGGER.warning(f"STCS - {self.device}")

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the switch off."""
        result = await self.execute_device_command(
            "main", self._capability, self._off_command, [self._off_value]
        )
        if result:
            self._internal_state[self._capability][self._attribute].value = self._of_value
            
        # State is set optimistically in the command above, therefore update
        # the entity state ahead of receiving the confirming push updates
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the switch on."""
        result = await self.execute_device_command(self._capability, self._on_command, [self._on_value])
        if result:
            self._internal_state[self._capability][self._attribute].value = self._on_value
        # State is set optimistically in the command above, therefore update
        # the entity state ahead of receiving the confirming push updates
        self.async_write_ha_state()

    @property
    def is_on(self) -> bool:
        """Return true if switch is on."""
        if self._on_value is not None:
            if self.get_attribute_value(self._capability, self._attribute) == self._on_value:
                return True
            return False
        return  self.get_attribute_value(self._capability, self._attribute)

    @property
    def icon(self) -> str | None:
        return self._icon

class SamsungOfcLightSwitch(SmartThingsEntity, SwitchEntity):
    """add samsung ocf light switch"""
    
    def __init__(self, client: SmartThings, rooms: dict[str, str], device: FullDevice, capabilties: set[Capability]) -> None:
        """Init the class."""
        super().__init__(
            client=client,
            device=device,
            rooms=rooms,
            capabilities=capabilties
        )
        self._page = "/mode/vs/0"
        self._key = "x.com.samsung.da.options"
        self._on_value = ["Light_On"]
        self._off_value = ["Light_Off"]
        self._name = "Light"
        self._on_icon = "mdi:led-on"
        self._off_icon = "mdi:led-variant-off"
        _LOGGER.warning(f"SOLS - {self.device}")

    execute_state = False
    init_bool = False

    def startup(self):
        """Make sure that OCF page visits mode on startup"""
        tasks = []
        tasks.append(
            self.execute_device_command(
                Capability.EXECUTE,
                "execute",
                [self._page]
            )
        )
        asyncio.gather(*tasks)
     
    async def async_turn_off(self, **kwargs) -> None:
        """Turn the switch off."""
        await self.execute_device_command(
            Capability.EXECUTE,
            "execute",
            [self._page, {self._key: self._off_value}]
        )
        # if result:
        #     self._device.status.update_attribute_value(
        #         "data", {"payload": {self._key: self._off_value}}
        #     )
        #     self.execute_state = False
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the switch on."""
        await self.execute_device_command(
            Capability.EXECUTE,
            "execute",
            [self._page, {self._key: self._on_value}]
        )
        # if result:
        #     self._device.status.update_attribute_value(
        #         "data", {"payload": {self._key: self._on_value}}
        #     )
        #     self.execute_state = True
        self.async_write_ha_state()

    @property
    def is_on(self) -> bool:
        """Return true if switch is on."""
        if not self.init_bool:
            self.startup()
        if self.get_attribute_value(Capability.EXECUTE, Attribute.DATA)["href"] == self._page:
            self.init_bool = True
            output = self.get_attribute_value(Capability.EXECUTE, Attribute.DATA)["payload"][
                self._key
            ]
            if len(self._on_value) > 1:
                if self._on_value in output:
                    self.execute_state = True
                elif self._off_value in output:
                    self.execute_state = False
            else:
                if self._on_value[0] in output:
                    self.execute_state = True
                elif self._off_value[0] in output:
                    self.execute_state = False
        return self.execute_state

    @property
    def icon(self) -> str | None:
        if self.is_on:
            return self._on_icon
        return self._off_icon

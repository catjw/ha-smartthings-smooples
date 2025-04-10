"""Support for switches through the SmartThings cloud API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pysmartthings import Attribute, Capability, Command, SmartThings

from homeassistant.components.switch import (
    DOMAIN as SWITCH_DOMAIN,
    SwitchEntity,
    SwitchEntityDescription,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from homeassistant.components.smartthings import FullDevice, SmartThingsConfigEntry, switch
from homeassistant.components.smartthings.const import INVALID_SWITCH_CATEGORIES, MAIN
from homeassistant.components.smartthings.entity import SmartThingsEntity
from homeassistant.components.smartthings.util import deprecate_entity

# CAPABILITIES = (
#     Capability.SWITCH_LEVEL,
#     Capability.COLOR_CONTROL,
#     Capability.COLOR_TEMPERATURE,
#     Capability.FAN_SPEED,
# )

# AC_CAPABILITIES = (
#     Capability.AIR_CONDITIONER_MODE,
#     Capability.AIR_CONDITIONER_FAN_MODE,
#     Capability.TEMPERATURE_MEASUREMENT,
#     Capability.THERMOSTAT_COOLING_SETPOINT,
# )

# MEDIA_PLAYER_CAPABILITIES = (
#     Capability.AUDIO_MUTE,
#     Capability.AUDIO_VOLUME,
#     Capability.MEDIA_PLAYBACK,
# )

# SWITCH = switch.SmartThingsSwitchEntityDescription(
#     key=Capability.SWITCH,
#     status_attribute=Attribute.SWITCH,
#     name=None,
# )

# CAPABILITY_TO_COMMAND_SWITCHES: dict[
#     Capability | str, switch.SmartThingsCommandSwitchEntityDescription
# ] = {
#     Capability.CUSTOM_DRYER_WRINKLE_PREVENT: switch.SmartThingsCommandSwitchEntityDescription(
#         key=Capability.CUSTOM_DRYER_WRINKLE_PREVENT,
#         translation_key="wrinkle_prevent",
#         status_attribute=Attribute.DRYER_WRINKLE_PREVENT,
#         command=Command.SET_DRYER_WRINKLE_PREVENT,
#     )
# }
# CAPABILITY_TO_SWITCHES: dict[Capability | str, switch.SmartThingsSwitchEntityDescription] = {
#     Capability.SAMSUNG_CE_WASHER_BUBBLE_SOAK: switch.SmartThingsSwitchEntityDescription(
#         key=Capability.SAMSUNG_CE_WASHER_BUBBLE_SOAK,
#         translation_key="bubble_soak",
#         status_attribute=Attribute.STATUS,
#     ),
#     Capability.SWITCH: switch.SmartThingsSwitchEntityDescription(
#         key=Capability.SWITCH,
#         status_attribute=Attribute.SWITCH,
#         component_translation_key={
#             "icemaker": "ice_maker",
#         },
#     ),
# }


@dataclass(frozen=True, kw_only=True)
class SamsungOcfSwitchEntityDescription(SwitchEntityDescription):
    """Describe a SmartThings switch entity."""

    status_attribute: Attribute
    command: Command

@dataclass
class SmartThingsExecuteCommands:
    name: str
    page: str
    section: str
    on: str
    off: str
    
    @property
    def set_off(self) -> list[str, dict[str, list[str]]]:
        return [self.page, {self.section: [self.off]}]
    @property
    def set_on(self) -> list[str, dict[str, list[str]]]:
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
            in switch.INVALID_SWITCH_CATEGORIES
        )
        if (
            device.device.type == "OCF"
            and not media_player
            and not appliance
            and device.status[MAIN][Capability.OCF][Attribute.MANUFACTURER_NAME].value == "Samsung Electronics"
        ):
            model = device.status[MAIN][Capability.OCF][Attribute.MODEL_NUMBER].value.split("|")[0]
            print(model)
            if (
                Capability.EXECUTE
                # and device.device.device_id == "climate"
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
                            status_attribute=Attribute.DATA,
                            translation_key="light",
                            command=Command.EXECUTE,
                            # component_translation_key={
                            #     'none': "light",
                            # },
                        ),
                        capability=Capability.EXECUTE,
                        commands=SmartThingsExecuteCommands(
                            'Light',
                            'mode/vs/0', 
                            'x.com.samsung.da.options',
                            'Light_On',
                            'Light_Off',
                        ),
                    )
                )
    async_add_entities(entities)
    
    
class SamsungOcfSwitch(switch.SmartThingsSwitch, SmartThingsExecuteCommands):
    """Representation of a Samsung OCF switch."""
    
    entity_description: switch.SmartThingsCommandSwitchEntityDescription
    
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

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self.execute_device_command(
            'execute',
            'execute',
            self.commands.set_off
        )
        
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self.execute_device_command(
            'execute',
            'execute',
            self.commands.set_on
        )
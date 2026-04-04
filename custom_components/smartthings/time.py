"""Time platform for SmartThings."""

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from homeassistant.components.smartthings import FullDevice
from . import SmartThingsConfigEntry

from homeassistant.components.smartthings import time


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SmartThingsConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add time entities for a config entry."""
    await time.async_setup_entry(hass, entry, async_add_entities, SmartThingsDnDTime)

    """Define a SmartThings time entity."""

    entity_description: SmartThingsTimeEntityDescription

    def __init__(
        self,
        client: SmartThings,
        device: FullDevice,
        entity_description: SmartThingsTimeEntityDescription,
    ) -> None:
        """Initialize the time entity."""
        super().__init__(client, device, {Capability.CUSTOM_DO_NOT_DISTURB_MODE})
        self.entity_description = entity_description
        self._attr_unique_id = f"{device.device.device_id}_{MAIN}_{Capability.CUSTOM_DO_NOT_DISTURB_MODE}_{entity_description.attribute}_{entity_description.attribute}"

    async def async_set_value(self, value: time) -> None:
        """Set the time value."""
        payload = {
            "mode": self.get_attribute_value(
                Capability.CUSTOM_DO_NOT_DISTURB_MODE, Attribute.DO_NOT_DISTURB
            ),
            "startTime": self.get_attribute_value(
                Capability.CUSTOM_DO_NOT_DISTURB_MODE, Attribute.START_TIME
            ),
            "endTime": self.get_attribute_value(
                Capability.CUSTOM_DO_NOT_DISTURB_MODE, Attribute.END_TIME
            ),
        }
        await self.execute_device_command(
            Capability.CUSTOM_DO_NOT_DISTURB_MODE,
            Command.SET_DO_NOT_DISTURB_MODE,
            {
                **payload,
                self.entity_description.attribute: f"{value.hour:02d}{value.minute:02d}",
            },
        )

    @property
    def native_value(self) -> time:
        """Return the time value."""
        state = self.get_attribute_value(
            Capability.CUSTOM_DO_NOT_DISTURB_MODE, self.entity_description.attribute
        )
        return time(int(state[:2]), int(state[3:5]))
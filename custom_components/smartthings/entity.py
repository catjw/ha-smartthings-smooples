"""Support for SmartThings Cloud."""

from homeassistant.components.smartthings import entity


class SmartThingsEntity(entity.SmartThingsEntity):
    """Representation of a SmartThings entity."""


# for i in entity.__all__:
#     setattr(SmartThingsEntity, i, getattr(entity, i))
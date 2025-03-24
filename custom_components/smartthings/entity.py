"""Support for SmartThings Cloud."""

from homeassistant.components.smartthings import entity


class SmartThingsEntity(entity.SmartThingsEntity):
    pass

for i in entity.__all__:
    setattr(SmartThingsEntity, i, getattr(entity, i))
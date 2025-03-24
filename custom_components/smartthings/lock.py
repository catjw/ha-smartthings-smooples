"""Support for locks through the SmartThings cloud API."""

from homeassistant.components.smartthings import lock


class SmartThingsLock(lock.SmartThingsLock):
    pass

for i in lock.__all__:
    setattr(SmartThingsLock, i, getattr(lock, i))
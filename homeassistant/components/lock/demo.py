"""
homeassistant.components.lock.demo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Demo platform that has two fake locks.
"""
from homeassistant.components.lock import LockDevice
from homeassistant.const import STATE_LOCKED, STATE_UNLOCKED


# pylint: disable=unused-argument
def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """ Find and return demo locks. """
    add_devices_callback([
        DemoLock('Front Door', STATE_LOCKED),
        DemoLock('Kitchen Door', STATE_UNLOCKED)
    ])


class DemoLock(LockDevice):
    """ Provides a demo lock. """
    def __init__(self, name, state):
        self._name = name
        self._state = state

    @property
    def should_poll(self):
        """ No polling needed for a demo lock. """
        return False

    @property
    def name(self):
        """ Returns the name of the device if any. """
        return self._name

    @property
    def is_locked(self):
        """ True if device is locked. """
        return self._state == STATE_LOCKED

    def lock(self, **kwargs):
        """ Lock the device. """
        self._state = STATE_LOCKED
        self.update_ha_state()

    def unlock(self, **kwargs):
        """ Unlock the device. """
        self._state = STATE_UNLOCKED
        self.update_ha_state()

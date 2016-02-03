"""
custom_components.hello_world
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Implements the bare minimum that a component should implement.

Configuration:

To use the hello_word component you will need to add the following to your
configuration.yaml file.

hello_world:
"""
import logging
from homeassistant.const import EVENT_STATE_CHANGED, EVENT_TIME_CHANGED
from homeassistant.components.switch import DOMAIN as DOMAIN_SWITCH, SERVICE_TURN_ON, \
    SERVICE_TURN_OFF, STATE_ON, ENTITY_ID_ALL_SWITCHES, is_on, turn_off, turn_on

# The domain of your component. Should be equal to the name of your component
DOMAIN = "hello_world"

# List of component names (string) your component depends upon
DEPENDENCIES = []

_LOGGER = logging.getLogger(__name__)
EVENT_HELLOWORLD = "event_helloworld"

global i
def setup(hass, config):
    """ Setup our skeleton component.
        Args:
            hass: 公共实例
            config: 配置
    """
    # States are in the format DOMAIN.OBJECT_ID
    hass.states.set('hello_world.Hello_World', 'Works!'+config["hello_world"]["platform"])


    _LOGGER.info("Hello World Started")
    _LOGGER.info(hass.bus.listeners)

    def time_change(event):
        # _LOGGER.info("Time Change"+event.data['now'].ctime())
        # if hass.states.is_state(ENTITY_ID_ALL_SWITCHES,STATE_ON):
        #     hass.services.call(DOMAIN_SWITCH,SERVICE_TURN_OFF)
        # else:
        #     hass.services.call(DOMAIN_SWITCH,SERVICE_TURN_ON)
        hass.states.set('hello_world.Hello_World2', 'Works Too!'+str(event.data))
        # hass.bus.fire(EVENT_HELLOWORLD,1)

    hass.bus.listen(EVENT_TIME_CHANGED, time_change)


    def customEventHandle(event):
        _LOGGER.info(event.event_type)

    hass.bus.listen(EVENT_HELLOWORLD, customEventHandle)



    def track_state_change(entity_id, old_state, new_state):
        _LOGGER.info(str(old_state)+" "+str(new_state))

    import homeassistant.helpers as helper
    helper.event.track_state_change(hass,'hello_world.Hello_World2',track_state_change)

    _LOGGER.info(hass.services.services)

    # return boolean to indicate that initialization was successful
    return True

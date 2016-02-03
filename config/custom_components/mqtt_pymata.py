"""
custom_components.mqtt_example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Shows how to communicate with MQTT. Follows a topic on MQTT and updates the
state of an entity to the last message received on that topic.

Also offers a service 'set_state' that will publish a message on the topic that
will be passed via MQTT to our message received listener. Call the service with
example payload {"new_state": "some new state"}.

Configuration:

To use the mqtt_example component you will need to add the following to your
configuration.yaml file.

mqtt_example:
  topic: home-assistant/mqtt_example

"""
import homeassistant.loader as loader
from pymata_aio.pymata_core import PymataCore
from pymata_aio.constants import Constants
from homeassistant.const import EVENT_STATE_CHANGED, EVENT_TIME_CHANGED
from homeassistant.components.switch import DOMAIN as DOMAIN_SWITCH, SERVICE_TURN_ON, \
    SERVICE_TURN_OFF, STATE_ON, ENTITY_ID_ALL_SWITCHES, is_on, turn_off, turn_on

# The domain of your component. Should be equal to the name of your component
DOMAIN = "mqtt_pymata"

# List of component names (string) your component depends upon
DEPENDENCIES = ['mqtt']

CONF_TOPIC = 'topic'
DEFAULT_TOPIC = 'home-assistant/mqtt_pymata'

DEFAULT_NAME = "MQTT Switch"
DEFAULT_QOS = 0
DEFAULT_PAYLOAD_ON = "ON"
DEFAULT_PAYLOAD_OFF = "OFF"
DEFAULT_OPTIMISTIC = False
DEFAULT_RETAIN = False


def setup(hass, config):
    """ Setup our mqtt_example component. """
    mp = Mqtt_Pymata(hass,
                     "state_topic",
                     "command_topic",
                     DEFAULT_QOS,
                     DEFAULT_RETAIN,
                     DEFAULT_PAYLOAD_ON,
                     DEFAULT_PAYLOAD_OFF,
                     DEFAULT_OPTIMISTIC,
                     0)
    return True


class Mqtt_Pymata:
    def __init__(self, hass, state_topic, command_topic, qos, retain,
                 payload_on, payload_off, optimistic, value_template):
        """

        @return:
        """
        self.hass = hass
        self._mqtt = loader.get_component('mqtt')
        self._switch = loader.get_component("switch")
        self._hass = hass
        self._state_topic = state_topic
        self._command_topic = command_topic
        self._qos = qos
        self._retain = retain
        self._payload_on = payload_on
        self._payload_off = payload_off
        self._optimistic = optimistic

        def command_recevie(topic, payload, qos):
            if payload == payload_on:
                self.turn_on()
            elif payload == payload_off:
                self.turn_off()

        self._mqtt.subscribe(hass, command_topic, command_recevie)

    def turn_on(self):
        """

        @return:
        """
        self._switch.turn_on(self._hass,"switch.ac")
        self._mqtt.publish(self.hass, self._state_topic, self._payload_on,
                     self._qos, self._retain)

    def turn_off(self):
        """

        @return:
        """
        self._switch.turn_off(self._hass,"switch.ac")
        self._mqtt.publish(self.hass, self._state_topic, self._payload_off,
                     self._qos, self._retain)

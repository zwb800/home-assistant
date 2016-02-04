from mqtt2pymata.mqtt_pymata import Mqtt_Pymata


CONF_TOPIC = 'topic'
DEFAULT_TOPIC = 'home-assistant/mqtt_switch'

DEFAULT_NAME = "MQTT Switch"
DEFAULT_PORT = 1883
DEFAULT_KEEPALIVE = 60
DEFAULT_QOS = 0
DEFAULT_PAYLOAD_ON = "ON"
DEFAULT_PAYLOAD_OFF = "OFF"
DEFAULT_OPTIMISTIC = False
DEFAULT_RETAIN = False


print("init...")
Mqtt_Pymata(DEFAULT_NAME,
            "127.0.0.1",
            DEFAULT_PORT,
            DEFAULT_KEEPALIVE,
            "state_arduino_switch",
            "command_arduino_switch",
            DEFAULT_QOS,
            DEFAULT_RETAIN,
            DEFAULT_PAYLOAD_ON,
            DEFAULT_PAYLOAD_OFF,
            DEFAULT_OPTIMISTIC,
            0,
            'COM3',
            13)
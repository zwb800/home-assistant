
import time
import paho.mqtt.client as mqtt
from PyMata.pymata import PyMata
from pymata_aio.pymata_core import PymataCore

PIN_MODE = 0  # This is the PyMata Pin MODE = ANALOG = 2 and DIGITAL = 0x20:
PIN_NUMBER = 1
DATA_VALUE = 2

class Mqtt_Pymata:
    def __init__(self,  name, broker, port, keepalive, state_topic, command_topic, qos, retain,
                 payload_on, payload_off, optimistic, value_template,serial_port,switch_pin):
        self._switch_pin = switch_pin
        self._board = PyMata(serial_port,False,verbose=True)
        self._board.set_pin_mode(self._switch_pin,self._board.OUTPUT,self._board.DIGITAL)

        A0 = 7
        def pin_callback(data):
            print("Analog Data: ",
                  " Pin: ", data[PIN_NUMBER],
                  " Pin Mode: ", data[PIN_MODE],
                  " Data Value: ", data[DATA_VALUE])
            self._board.set_analog_latch(A0,self._board.ANALOG_LATCH_GT,500,pin_callback)


        self._board.set_pin_mode(A0, self._board.INPUT, self._board.ANALOG)
        self._board.set_sampling_interval(100)
        self._board.set_analog_latch(A0,self._board.ANALOG_LATCH_GT,500,pin_callback)

        # while True:
        #     time.sleep(0.1)
        #     value = self._board.analog_read(A0)
        #     print(value)

        self._mqtt = mqtt.Client()

        self._switch = None
        self._state_topic = state_topic
        self._command_topic = command_topic
        self._qos = qos
        self._retain = retain
        self._payload_on = payload_on
        self._payload_off = payload_off
        self._optimistic = optimistic
        self._state = False

        def on_message( _mqtt, userdata, msg):
            topic = msg.topic,
            qos = msg.qos,
            payload = msg.payload.decode('utf-8'),
            payload = payload[0]
            print(msg.topic+" "+payload)

            if payload == payload_on:
                self.turn_on()
            elif payload == payload_off:
                self.turn_off()

        self._mqtt.on_message = on_message
        self._mqtt.connect(broker, port, keepalive)
        self._mqtt.subscribe(command_topic,qos)
        self._mqtt.loop_forever()

    def turn_on(self):
        self._state = True
        self.apply_state()
        self.report_state()

    def turn_off(self):
        self._state = False
        self.apply_state()
        self.report_state()

    def apply_state(self):
        self._board.digital_write(self._switch_pin,self._board.HIGH if self._state else self._board.LOW)

    def report_state(self):
        self._mqtt.publish( self._state_topic, self._payload_on if self._state else self._payload_off,
                     self._qos, self._retain)

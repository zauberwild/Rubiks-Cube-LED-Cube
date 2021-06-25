from machine import Pin
import time

""" pins """
data_pin, clock_pin, latch_pin = Pin(20, Pin.OUT), Pin(19, Pin.OUT), Pin(21, Pin.OUT)
led_pin = Pin(28, Pin.OUT)

""" led mapping """
# index is the number of led if counted through correctly,
# value the actual pin on the registers
# if value equal to -1, actual pin is equal to counted leds
led_map = list(range(25))
led_map[9] = 10
led_map[10] = 11
led_map[11] = 12
led_map[12] = 13
led_map[13] = 14
led_map[14] = 15
led_map[15] = 9
led_map[21] = 23
led_map[23] = 21


""" state of the leds """
states = [0] * 25

""" functions """
def set(led, state):
	""" set an led to given state
	- out: led to set (0-24)
	- state: state of the led (0: off, 1: on)
	NOTE: this function doesn't change the leds. to apply changes, use write()
	"""
	# change led to the real pin
	led = led_map[led]

	states[led] = state	

def write():
	""" writes all leds to new state """

	latch_pin.low()

	for i in states[-2::-1]:			# go backwards, because the bits are shifted/pushed through the register 
									# (leave the last state out, as it is written separately)
		
		if i:								# write data pin
			data_pin.high()
		else:
			data_pin.low()

		clock_pin.high()			# emit clock signal to shift the bits
		clock_pin.low()

	data_pin.low()
	latch_pin.high()				# write to output registers
	
	if states[-1]:					# write last led on top
		led_pin.high()
	else:
		led_pin.low()

	
def clear(write_directly=False):
	""" set all outputs to zero
	- write_directly=False: set to True to directly write to the registers
	"""
	for idx, val in enumerate(states):
		states[idx] = 0

	if write_directly:
		write()
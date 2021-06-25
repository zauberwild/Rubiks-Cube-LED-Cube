""" Rubiks-Cube-LED-Cube

A cube full of blinking red LEDs controlled by Raspberry Pi Pico and this Software

Author: zauberwild
Copyright: zauberwild 2021 Released under the MIT license
"""

""" ### ### IMPORTS ### ### """
import modes
from machine import Pin
import led
from ir_rx.nec import NEC_8  		# NEC remote, 8 bit addresses
import ir_receiver as ir_lib
import random



""" ### ### VARIABLES ### ### """
mode = 2
ir_pin = 22

prev_received_data = 0

""" ### ### MODES ### ### """
modes = [modes.M0(), modes.M1(), modes.M2(), modes.M3(), modes.M4(),
		 modes.M5(), modes.M6(), modes.M7(), modes.M8(), modes.M9(), modes.M_star()]



""" ### ### FUNCTIONS ### ### """
def ir_callback(data, addr, ctrl):
	""" this function will be called, as soon the ir receiver gets some input
	"""
	global prev_received_data, mode

	# change mode / received a number
	if data in ir_lib.k_num:
		num = 0
		for idx, val in enumerate(ir_lib.k_num):
			if val == data:
				num = idx
		mode = num
		modes[mode].start()
		print("[ir_callback] changed mode to:", mode)
	
	# random mode
	if data == ir_lib.k_hashtag:
		mode = random.randrange(0, 10)
		print("[ir_callback] random mode generated")
		print("[ir_callback] changed mode to:", mode)
		modes[mode].start()

	# experimental pwm-emulation (accessible via the star / asterisk)
	if data == ir_lib.k_star:
		mode = 10
		print("[ir_callback] testing experimental PWM emulation")
	
	if data == ir_lib.k_up:							# speeding things up
		print("[ir_callback] increased speed")
		modes[mode].increase_speed()
	elif data == ir_lib.k_down:						# slowing down
		print("[ir_callback] decreased speed")
		modes[mode].decrease_speed()


""" ### ### OBJECTS ### ### """

ir = NEC_8(Pin(ir_pin, Pin.IN), ir_callback)



""" ### ### SETUP ### ### """
print("LED-Cube starting")
led.clear(write_directly=True)



""" ### ### LOOP ### ### """
while True:
	
	modes[mode].update()


	



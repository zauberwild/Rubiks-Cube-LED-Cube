""" 
this file saves all variables and objects, that need to be accessed to globally
"""

from machine import Pin
from ir_rx.nec import NEC_8  # NEC remote, 8 bit addresses


""" ### ### VARIABLES ### ### """
mode = 0
ir_pin = 22


indicator_increase, indicator_decrease = False, False
indicator_mode_change = False


prev_received_data = 0

""" ### ### FUNCTIONS ### ### """
def ir_callback(data, addr, ctrl):
	""" this function will be called, as soon the ir receiver gets some input
	"""
	global indicator_increase, indicator_decrease, indicator_mode_change
	global prev_received_data, mode

	if data == -1 and not prev_received_data in ir_rx.k_num:
		data = prev_received_data

	if data in ir_rx.k_num:							# change mode
		num = 0
		for idx, val in enumerate(ir_rx.k_num):
			if val == data:
				num = idx
		mode = num
		indicator_mode_change = True
		print("[ir_callback] changed mode to:", mode)
	
	if data == ir_rx.k_up:							# speeding things up
		print("[ir_callback] increased speed")
		indicator_increase = True
	elif data == ir_rx.k_down:						# slowing down
		print("[ir_callback] decreased speed")
		indicator_decrease = True

	if data != -1:
		prev_received_data = data


""" ### ### OBJECTS ### ### """

ir = NEC_8(Pin(ir_pin, Pin.IN), ir_callback)

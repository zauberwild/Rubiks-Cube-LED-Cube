#import globals as gl
import utime
import led
import random


class M_blueprint:

	def __init__(self):
		self.finish_time = 0
		self.state = False
		self.frame_duration = 250

	def start(self):
		""" call this to start a mode """
		led.clear(write_directly=True)

	def update(self):
		""" needs to be called repeatedly. no time.sleep() or similar """

		t = utime.ticks_ms()
		if t > self.finish_time:
			self.finish_time = t + self.frame_duration

			self.state = not self.state

			led.set(0, self.state)
			led.set(1, not self.state)
			led.write()

	def increase_speed(self):
		self.frame_duration -= 100

		if self.frame_duration < 100:
			self.frame_duration = 100
		print("[m_blueprint | increase_speed] frame duration now at", self.frame_duration)

	def decrease_speed(self):
		self.frame_duration += 100

		if self.frame_duration > 2000:
			self.frame_duration = 2000
		print("[m_blueprint | decrease_speed] frame duration now at", self.frame_duration)

class M0(M_blueprint):		# clear all leds / "off"
	def update(self):
		""" do nothing and stay calm """
		pass



class M1(M_blueprint):		# fill up (moving through led indices)
	def __init__(self):
		self.finish_time = 0
		self.filling = True
		self.number_leds = len(led.states)
		self.current_led = 0
		self.frame_duration = 200

	def start(self):
		""" call this to start a mode """
		led.clear(write_directly=True)
		self.filling = True
		self.current_led = 0
	
	def update(self):
		""" needs to be called repeatedly. no time.sleep() or similar """

		t = utime.ticks_ms()
		if t > self.finish_time:
			self.finish_time = t + self.frame_duration

			led.set(self.current_led, self.filling)
			led.write()

			self.current_led += 1

			if self.current_led >= self.number_leds:
				self.current_led = 0
				self.filling = not self.filling

	def increase_speed(self):
		if self.frame_duration >= 200:
			self.frame_duration -= 100
		else:
			self.frame_duration -= 20

		if self.frame_duration < 0:
			self.frame_duration = 0
		print("[m1 | increase_speed] frame duration now at", self.frame_duration)
	
	def decrease_speed(self):
		if self.frame_duration >= 200:
			self.frame_duration += 100
		else:
			self.frame_duration += 20

		if self.frame_duration > 2000:
			self.frame_duration = 2000
		print("[m1 | decrease_speed] frame duration now at", self.frame_duration)



class M2(M_blueprint):		# random leds blinking
	""" random leds """

	# table for different velocities of the animation
	speed = 10
	new_led_lower = [936, 893, 850, 806, 763, 720, 676, 633, 590, 546, 503, 460, 416, 373, 330, 286, 243, 200, 156, 113, 70]
	new_led_upper = [2040, 1946, 1851, 1757, 1662, 1568, 1474, 1379, 1285, 1191, 1096, 1002, 908, 813, 719, 624, 530, 436, 341, 247, 153]
	dur_led_lower = [2164, 2064, 1964, 1864, 1764, 1663, 1563, 1463, 1363, 1263, 1163, 1063, 963, 863, 763, 662, 562, 462, 362, 262, 162]
	dur_led_upper = [10000, 9537, 9075, 8612, 8150, 7687, 7225, 6762, 6300, 5837, 5375, 4912, 4449, 3987, 3524, 3062, 2599, 2137, 1674, 1212, 750]


	def __init__(self):
		self.finish_time = []
		self.random_leds = []
		self.number_leds = len(led.states)

		self.random_time = utime.ticks_ms() + self.get_random_time(new_led=True)

	def start(self):
		print("[m2 | start] m2 running")
		# reset everything
		led.clear(write_directly=True)
		self.finish_time.clear()
		self.random_leds.clear()
	
	def update(self):

		t = utime.ticks_ms()
		if t > self.random_time:
			# restart timer
			self.random_time = utime.ticks_ms() + self.get_random_time(new_led=True)

			# add new led
			self.finish_time.append(utime.ticks_ms() + self.get_random_time())
			random_led = random.randrange(0,self.number_leds)
			self.random_leds.append(random_led)
			led.set(random_led, 1)
			led.write()

		clearing_list = [] 			# store the indexes of times to be deleted her
		
		if len(self.finish_time) > 0:
			for i in range(len(self.finish_time)-1):
				if t > self.finish_time[i]:
					# turn led off
					led.set(self.random_leds[i], 0)
					led.write()

					# remove from lists
					clearing_list.append(i)
		
		for i in clearing_list:
			self.finish_time.pop(i)
			self.random_leds.pop(i)
		
	
	def get_random_time(self, new_led = False):
		""" new_led: set true when needing a time for new led, not duration """
		if new_led:
			l = self.new_led_lower[self.speed]
			u = self.new_led_upper[self.speed]
		else:
			l = self.dur_led_lower[self.speed]
			u = self.dur_led_upper[self.speed]

		return random.randrange(l, u)
	
	def increase_speed(self):
		self.speed += 1

		if self.speed > len(self.new_led_lower)-1:
			self.speed = len(self.new_led_lower)-1

		print("[m2 | increase_speed] speed now at stage:", self.speed)

	def decrease_speed(self):
		self.speed -= 1

		if self.speed < 0:
			self.speed = 0

		print("[m2 | decrease_speed] speed now at stage:", self.speed)

	

class M3(M_blueprint):		# lighthouse mode
	def __init__(self):
		self.finish_time = 0
		self.number_leds = 8
		self.current_led_on = [22, 18, 14, 10, 6, 2]
		self.frame_duration = 200

	def start(self):
		""" call this to start a mode """
		led.clear(write_directly=True)
		self.current_led = 0
	
	def update(self):
		""" needs to be called repeatedly. no time.sleep() or similar """

		t = utime.ticks_ms()
		if t > self.finish_time:
			self.finish_time = t + self.frame_duration

			# upper layer		
			for i in self.current_led_on[0:2]:
				led.set(i, 1)
				off = i-1
				if off < 16:
					off += 8
				led.set(off, 0)

				idx = self.current_led_on.index(i)
				self.current_led_on[idx]+=1
				if(self.current_led_on[idx]>23):
					self.current_led_on[idx]=16
			
			# middle layer
			for i in self.current_led_on[2:4]:
				led.set(i, 1)
				off = i-1
				if off < 8:
					off += 8
				led.set(off, 0)

				idx = self.current_led_on.index(i)
				self.current_led_on[idx]+=1
				if(self.current_led_on[idx]>15):
					self.current_led_on[idx]=8

			# lower layer
			for i in self.current_led_on[4:6]:
				led.set(i, 1)
				off = i-1
				if off < 0:
					off += 8
				led.set(off, 0)

				idx = self.current_led_on.index(i)
				self.current_led_on[idx]+=1
				if(self.current_led_on[idx]>7):
					self.current_led_on[idx]=0

			led.write()

	def increase_speed(self):
		if self.frame_duration >= 200:
			self.frame_duration -= 100
		else:
			self.frame_duration -= 20

		if self.frame_duration < 0:
			self.frame_duration = 0
		print("[m1 | increase_speed] frame duration now at", self.frame_duration)
	
	def decrease_speed(self):
		if self.frame_duration >= 200:
			self.frame_duration += 100
		else:
			self.frame_duration += 20

		if self.frame_duration > 2000:
			self.frame_duration = 2000
		print("[m1 | decrease_speed] frame duration now at", self.frame_duration)



class M4(M_blueprint):
	pass



class M5(M_blueprint):
	pass



class M6(M_blueprint):
	pass



class M7(M_blueprint):			# flooding from random point
	def __init__(self):
		self.finish_time = 0
		self.state = False					# True when flooding with leds on, False when flooding with leds off
		self.frame_duration = 400
		self.get_new_starting_point = False
		self.border_leds = []

	def start(self):
		""" call this to start a mode """
		led.clear(write_directly=True)
		self.get_new_starting_point = True

	def update(self):
		""" needs to be called repeatedly. no time.sleep() or similar """

		t = utime.ticks_ms()
		if t > self.finish_time:
			self.finish_time = t + self.frame_duration

			# find a new starting point if necessary
			if self.get_new_starting_point:
				self.get_new_starting_point = False
				#print("finding new start point")
				self.border_leds.clear()
				self.border_leds.append(random.randrange(0,25))
				self.state = not self.state
			
			
			# clear border leds and keep them in local variable
			b_leds = self.border_leds.copy()
			self.border_leds.clear()

			# delete any duplicates
			b_leds = list(dict.fromkeys(b_leds))

			# check every led on border between on and off
			for i in b_leds:
				#print("now checking border_led number", i)
				surrounding_leds = [i-1, i+1, i-8, i+8]			# get neighboring leds
				
				# check each neighbor
				for j in surrounding_leds:
					# check if led is existent
					if j < 0:
						continue
					elif j > 24:
						j = 24

					#print("now checking neighbor_led number", j)
					# test if new led, thus led being on the border
					if led.states[j] != self.state:
						self.border_leds.append(j)

					# set to state
					led.set(j, self.state)
			
			# look for unchanged leds
			all_leds_changed = True
			for i in led.states:
				if i != self.state:
					all_leds_changed = False
			
			if all_leds_changed:
				self.get_new_starting_point = True
				#print("all leds set")

			# write to leds
			led.write()


	def increase_speed(self):
		self.frame_duration -= 100

		if self.frame_duration < 100:
			self.frame_duration = 100
		print("[m7 | increase_speed] frame duration now at", self.frame_duration)

	def decrease_speed(self):
		self.frame_duration += 100

		if self.frame_duration > 2000:
			self.frame_duration = 2000
		print("[m7 | decrease_speed] frame duration now at", self.frame_duration)



class M8(M_blueprint):
	pass



class M9(M_blueprint):
	pass


class M_star(M_blueprint):		# experimental pwm
	def __init__(self):
		self.finish_time = 0
		self.state = False
		self.frame_on = 5
		self.frame_off = 5
		self.max_time = 10
		self.step_size = 0.1

		self.sweep_duration = 10
		self.sweep_finish_time = 0
		self.sweep_brighter = True

	def start(self):
		""" call this to start a mode """
		led.clear(write_directly=True)

	def update(self):
		""" needs to be called repeatedly. no time.sleep() or similar """

		t = utime.ticks_ms()
		if t > self.finish_time:
			if self.state:
				self.finish_time = t + self.frame_off
			else:
				self.finish_time = t + self.frame_on

			
			self.state = not self.state

			for i in range(25):
				led.set(i, self.state)
			led.write()

		# automatic sweep
		
		if t > self.sweep_finish_time:
			self.sweep_finish_time = t + self.sweep_duration

			if self.sweep_brighter:
				self.increase_speed()
			else:
				self.decrease_speed()
			
			if self.frame_on == 0:
				self.sweep_brighter = True
			if self.frame_off == 0:
				self.sweep_brighter = False
		

	def increase_speed(self):
		self.frame_on += self.step_size

		if self.frame_on > self.max_time:
			self.frame_on = self.max_time

		self.frame_off = self.max_time - self.frame_on

		#print("[m_blueprint | increase_speed] frame on / off time now at", self.frame_on, "/", self.frame_off)

	def decrease_speed(self):
		self.frame_on -= self.step_size

		if self.frame_on < 0:
			self.frame_on = 0
		
		self.frame_off = self.max_time - self.frame_on

		#print("[m_blueprint | decrease_speed] frame on / off time now at", self.frame_on, "/", self.frame_off)

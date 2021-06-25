import led
import utime

led.clear(write_directly = True)

all = True

if all:
	filling = True

	l = 0

	while True:

		led.set(l, int(filling))
		#print("now set led", l, "to", filling)

		led.write()
		#print(led.states)

		l += 1

		if l > 24:
			l = 0
			filling = not filling

		utime.sleep(0.15)

else:
	s = True

	while True:
		led.set(18, int(s))
		led.write()

		print("led is", s)
		print(led.states)

		utime.sleep(0.5)
		s = not s

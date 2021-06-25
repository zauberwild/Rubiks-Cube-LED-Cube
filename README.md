# RUBIKS CUBE LED CUBE

I ripped an old led cube apart and placed my own leds, shift registers and Raspberry Pi Pico in it. The cube displays some small animations, between which you can choose with an ir-remote.



*This project is licensed under the MIT license (2021 by zauberwild)*

## MODES

1. Fill up. each led is switched on one after the other, then turned off one after the other.
2. Random. leds will be randomly turned onn, and after a random time turned off.
3. lighthouse. to beams going round around the cube
4. filling in layers - *WIP*
5. random blocks - *WIP*
6. rain - *WIP*
7. flood-fill. starts in a specific point, flooding the whole cube.
8. snake - *WIP*

- '0' turns all leds off
- '#' starts a random mode
- '*' shows an experimental PWM-ish feature on the leds. It is experimental and doesn't really run smoothly
- You can control the speed of the animations with the *UP* and *DOWN* arrow keys





## PINOUT RASPBERRY PI PICO

- top led: 28
- ir: 22



## BOM  (ORDERED)

- [x] LED Rubiks Cube
- [x] (red) LEDs, 25x [link](https://www.berrybase.de/bauelemente/aktive-bauelemente/leds/standard-leds/optosupply-round-super-led-5mm-rot)
- [x] Resistors (220 Ohm) , 25x [link](https://www.berrybase.de/bauelemente/passive-bauelemente/widerstaende/metallschichtwiderstaende/0-25w-1/metallschichtwiderstand-1/4w-177-1-0207-axial-durchsteckmontage?number=MSW220R.25)
- [x] PCB (20 columns x 14 rows)
- [x] Raspberry Pi Pico
- [x] Shift-Register, 3x [link](https://www.berrybase.de/bauelemente/aktive-bauelemente/ics/ics-s../sn74hc595n-8-bit-schieberegister-dil-16)
- [x] USB-Cable (Type A <-> single Wires (VCC & GND)) [link](https://www.berrybase.de/computer/kabel-adapter/usb/usb-a/kabel-usb-typ-a-stecker-150-2x-pfostenstecker-einzeln-zur-stromversorgung?number=D85402)
- [x] IR-Sensor and IR-Remote

## BOM (PRINTED)

- [x] 4x middle.stl
- [x] 4x vertical_edge.stl
- [x] 8x horizontal_edge.stl
- [x] 8x corner.stl
- [x] 1x top.stl
- [x] 1x base.stl



## CREDIT WHERE CREDIT IS DUE

### ir_rx

This folder is part of a micropython module for ir-communication. Published by Peter Hinch on [GitHub](https://github.com/peterhinch/micropython_ir) under the MIT license.


Pi Word Clock
==============

My 7 and 8yr old kids wanted to get started with electronics and programming,
 so we started off with an LED word clock.

[![Raspberry Pi Word Clock](http://img.youtube.com/vi/Dd1wtXz80Cs/0.jpg)]
(http://www.youtube.com/watch?v=Dd1wtXz80Cs)

Code & Images for making Word Clocks included. We used Raspberry Pi and 8x8 matrix. Works with I2C Adafruit Backpack and the Unicorn Hat from Pimoroni.

Code is Python & will possibly add a C version.

There are 8x8 fonts included and the ability to scroll messages or animate frames of 8x8 sprites. There is a tool at http://gurgleapps.com/tools/matrix which makes it easy to design 8x8 sprites and get the HEX code out.

The code has a demo
mode to run through times, and takes command line arguments to set brightness and I2C
address etc.

Template inspired by Daniel Rojas https://github.com/formatc1702/Micro-Word-Clock

Starting with an Adafruit LED backpack via I2C may support others soon.

https://learn.adafruit.com/adafruit-led-backpack/overview

You can buy transparency paper for inkjet printers but even regular printer paper
works quite well.

Instructions to get i2c working on a pi are [here](docs/new_pi_setup.md)


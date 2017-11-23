# nxttools.hardware -- module that provides euphemisms for nxt devices in different formats
# Copyright (C) 2017 Ryan B Au
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import nxt, thread, time
from nxt.sensor.hitechnic import *

class DcMotor(MotorCon):
    def __init__(self, brick, port, motorport):
        """Creates a hitechnic Dc Motor object where 
        brick is the nxt brick object
        port is the nxt port value (ie. nxt.PORT_1)
        motorport is an integer port value on the motor controller"""
        super(DcMotor,self).__init__(brick, port)
        self.motorport = motorport
    def set_power(self,power):
        """power is originally -100 to 100
        use decimal value -1 to 1"""
        super(DcMotor,self).set_power(self.motorport,power*100.0)
    def setPower(self,power):
        """power is originally -100 to 100
        use decimal value -1 to 1"""
        self.set_power(power)
    def get_power(self):
        """power is originally -100 to 100
        return decimal value -1 to 1"""
        return super(DcMotor,self).get_power(self.motorport)/100.0
    def getPower(self,power):
        """power is originally -100 to 100
        return decimal value -1 to 1"""
        return self.get_power()
    def set_enc_target(self, val):
        """Encoder target can be an integer value.  
        1440 encoders represents 360 degrees, one full rotation."""
        super(DcMotor,self).set_enc_target(self.motorport,val)
    def get_enc_target(self):
        """Encoder target returned will be an integer value.  
        1440 encoders represents 360 degrees, one full rotation."""
        return super(DcMotor,self).get_enc_target(self.motorport)
    def get_enc_current(self):
        """Encoder returned will be an integer value.  
        1440 encoders represents 360 degrees, one full rotation."""
        return super(DcMotor,self).get_enc_current(self.motorport)
    def get_battery_voltage(self):
        """Returns battery voltage read by the motor controller 
        connected to this motor"""
        return super(DcMotor,self).get_battery_voltage()
    def set_mode(self,mode):
        """modes:
        1 - Run with power control only
        2 - Run with constant speed
        3 - Run to position
        4 - Reset current encoder"""
        modes = [0x00,0x01,0x02,0x03]
        super(DcMotor,self).set_mode(self.motorport,modes[mode-1])

class Servo(ServoCon):
    def __init__(self, brick, port, servoport):
        """Creates hitechnic Servo object where 
        brick is the nxt brick object
        port is the nxt port that connects to the servo controller
        servoport is a port number (1-6) on the servo controller"""
        super(Servo,self).__init__(brick,port)
        self.servoport = servoport
    def set_pos(self, pos):
        """pos(position) is originally (0 to 255)
        """
        super(Servo,self).set_pos(self.servoport, pos)
    def setPosition(self, pos):
        """pos(position) is originally (0 to 255)
        """
        self.set_pos(pos)

# nxttools.gamepad -- interface to access gamepad controls
# Copyright (C) 2017 Ryan B Au
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import inputs, thread
import rangetools


class ul_Gamepad(object):
    """This is the blueprint for gamepads in the unordered list.
    This unordered list contains a random list of gamepads as they
    are added onto the computer"""
    start = False #BTN_START    
    back = False #BTN_SELECT
    guide = False #BTN_MODE    
    #Colorful buttons on right side
    a = False #BTN_SOUTH
    b = False #BTN_EAST
    x = False #BTN_NORTH
    y = False #BTN_WEST
    #Dpad on the left
    dpad_up = False    #ABS_HAT0Y,-1
    dpad_down = False  #ABS_HAT0Y, 1
    dpad_left = False  #ABS_HAT0X,-1
    dpad_right = False #ABS_HAT0X, 1
    #Shoulder buttons
    left_bumper = False    #BTN_TL
    right_bumper = False   #BTN_TR
    left_trigger  = 0 #ABS_Z
    right_trigger = 0 #ABS_RZ

    #Joysticks
    left_stick_button = False   #BTN_THUMBL
    right_stick_button = False  #BTN_THUMBR
    left_stick_y = 0 #ABS_Y
    left_stick_x = 0 #ABS_X
    right_stick_y = 0 #ABS_RY
    right_stick_x = 0 #ABS_RX

    def __init__(self, x=None):
        """x -- the index of the gamepad from the unordered list of gamepads
        pregenerated by the computer (inputs)"""
        if x is not None:
            self.events = inputs.DeviceManager().gamepads[x]

    def update(self):
        """An infinite loop that changes this object's input properties as events are sent in"""
        while 1:
            for event in self.events.read():
                #Dpad on the left
                if(event.code=="ABS_HAT0Y"):
                    if(event.state==-1):
                        self.dpad_up = True
                    if(event.state==0):
                        self.dpad_down = False
                        self.dpad_up = False
                    if(event.state==1):
                        self.dpad_down = True
                if(event.code=="ABS_HAT0X"):
                    if(event.state==-1):
                        self.dpad_left = True
                    if(event.state==0):
                        self.dpad_right = False
                        self.dpad_left = False
                    if(event.state==1):
                        self.dpad_right = True
                #Colorful Buttons on the right
                if(event.code=="BTN_SOUTH"):
                    if(event.state==1):
                        self.a = True
                    if(event.state==0):
                        self.a = False
                if(event.code=="BTN_EAST"):
                    if(event.state==1):
                        self.b = True
                    if(event.state==0):
                        self.b = False
                if(event.code=="BTN_NORTH"):
                    if(event.state==1):
                        self.x = True
                    if(event.state==0):
                        self.x = False
                if(event.code=="BTN_WEST"):
                    if(event.state==1):
                        self.y = True
                    if(event.state==0):
                        self.y = False
                #Buttons in the center part
                if(event.code=="BTN_START"):
                    if(event.state==1):
                        self.start = True
                    if(event.state==0):
                        self.start = False
                if(event.code=="BTN_MODE"):
                    if(event.state==1):
                        self.guide = True
                    if(event.state==0):
                        self.guide = False
                if(event.code=="BTN_SELECT"):
                    if(event.state==1):
                        self.back = True
                    if(event.state==0):
                        self.back = False
                #Joysticks
                if(event.code=="ABS_Y"):
                    self.left_stick_y = rangetools.clip((event.state+129)/32600.0,-1,1)
                if(event.code=="ABS_X"):
                    self.left_stick_x = rangetools.clip((event.state-128)/32600.0,-1,1)
                if(event.code=="ABS_RY"):
                    self.right_stick_y = rangetools.clip((event.state+129)/32600.0,-1,1)
                if(event.code=="ABS_RX"):
                    self.right_stick_x = rangetools.clip((event.state-128)/32600.0,-1,1)
                if(event.code=="BTN_THUMBR"):
                    if(event.state==1):
                        self.right_stick_button = True
                    if(event.state==0):
                        self.right_stick_button = False
                if(event.code=="BTN_THUMBL"):
                    if(event.state==1):
                        self.left_stick_button = True
                    if(event.state==0):
                        self.left_stick_button = False
                #Shoulder Buttons
                if(event.code=="ABS_Z"):
                    self.left_trigger = rangetools.clip((event.state)/255.0,0,1)
                if(event.code=="ABS_RZ"):
                    self.right_trigger = rangetools.clip((event.state)/255.0,0,1)
                if(event.code=="BTN_TL"):
                    if(event.state==1):
                        self.left_bumper = True
                    if(event.state==0):
                        self.left_bumper = False
                if(event.code=="BTN_TR"):
                    if(event.state==1):
                        self.right_bumper = True
                    if(event.state==0):
                        self.right_bumper = False
class ol_Gamepad(object):
    """This is the blueprint for a single gamepad object that contains an unordered list of gamepads
    and then picks on a single gamepad based on a button combination to take on its input properties.
    Essentially, this is a single player's controller, and the button combo assigns a gamepad to this player."""
    message = 0 #Gamepad Indicator message 3 state switch: int 0-2

    status0 = False
    status1 = False
    gamepads = []
    pad = ul_Gamepad()
    old = ul_Gamepad()
    numG = len(inputs.DeviceManager().gamepads)
    #center buttons
    start = False #BTN_START
    back = False #BTN_SELECT
    guide = False #BTN_MODE
    #Colorful buttons on right side
    a = False #BTN_SOUTH
    b = False #BTN_EAST
    x = False #BTN_NORTH
    y = False #BTN_WEST
    #Dpad on the left
    dpad_up = False    #ABS_HAT0Y,-1
    dpad_down = False  #ABS_HAT0Y, 1
    dpad_left = False  #ABS_HAT0X,-1
    dpad_right = False #ABS_HAT0X, 1
    #Shoulder buttons
    left_bumper = False    #BTN_TL
    right_bumper = False   #BTN_TR
    left_trigger  = 0 #ABS_Z
    right_trigger = 0 #ABS_RZ

    #Joysticks
    left_stick_button = False   #BTN_THUMBL
    right_stick_button = False  #BTN_THUMBR
    left_stick_y = 0 #ABS_Y
    left_stick_x = 0 #ABS_X
    right_stick_y = 0 #ABS_RY
    right_stick_x = 0 #ABS_RX

    def __init__(self,n):
        """n -- represents the player number that this objects identifies with.  This player number
        determines the button combination that this player's gamepad associates with"""
        self.id = n
    def button(self,x):
        """gives back the button associated with this player gamepad's id"""
        arr = "a b y x dpad_down dpad_right dpad_up dpad_down".split(" ")
        return arr[x]
    def other_buttons(self,x):
        """gives back all of the buttons that are not associated with this player gamepad's id"""
        arr = "a b y x dpad_down dpad_right dpad_up dpad_down".split(" ")
        del arr[x]
        return arr
    def status(self):
        """infinite loop that updates when this gamepad has been assigned or not"""
        while 1:
            if(self.status0==self.status1):
                if(not self.status0):
                    #print "Gamepad %d Unassigned" % (self.id+1)
                    
                if(self.status0):
                    print "Gamepad %d Assigned" % (self.id+1)
                self.message = 0
                self.status0 = not self.status1
    def update(self):
        """contains an infinite loop that takes the input properties of the 
        original gamepad from the unordered list and makes them its own. """
        for num in range(self.numG):
            self.gamepads.append(ul_Gamepad(num))
            thread.start_new_thread(self.gamepads[num].update,())
        print("Gamepad "+str(self.id+1)+" Initialized")
        while (self.id<=self.other_buttons(self.id)):
            for item in range(len(self.gamepads)):
                if(self.gamepads[item].start and self.gamepads[item].__dict__[self.button(self.id)]):
                    self.pad = self.gamepads[item]
                    self.status1 = True
                for f in range(len(self.other_buttons(self.id))):
                    if(self.pad.start and self.pad.__dict__[self.other_buttons(self.id)[f]]):
                        self.pad = self.old
                        self.status1 = False
            self.start = self.pad.start
            self.back = self.pad.back
            self.guide = self.pad.guide
            self.a = self.pad.a
            self.b = self.pad.b
            self.x = self.pad.x
            self.y = self.pad.y
            self.dpad_up = self.pad.dpad_up
            self.dpad_down = self.pad.dpad_down
            self.dpad_left = self.pad.dpad_left
            self.dpad_right = self.pad.dpad_right
            self.left_bumper = self.pad.left_bumper
            self.right_bumper = self.pad.right_bumper
            self.left_trigger = self.pad.left_trigger
            self.right_trigger = self.pad.right_trigger
            self.left_stick_button = self.pad.left_stick_button
            self.right_stick_button = self.pad.right_stick_button
            self.left_stick_y = self.pad.left_stick_y
            self.left_stick_x = self.pad.left_stick_x
            self.right_stick_y = self.pad.right_stick_y
            self.right_stick_x = self.pad.right_stick_x


    def updater(self):
        thread.start_new_thread(self.update,())
        thread.start_new_thread(self.status,())
    def toStr_bool(self):
        arr = "start back guide a b x y dpad_up dpad_down dpad_left dpad_right left_bumper right_bumper left_stick_button right_stick_button".split(" ")
        s = ""
        for i in arr:
            if self.__dict__[i]:
                s += i
                s += " "
        return s
    def toStr_float(self):
        arr = "left_trigger right_trigger left_stick_y left_stick_x right_stick_y right_stick_x".split(" ")
        s = ""
        for i in arr:
            s += i + ":"
            s += str(self.__dict__[i])
            s += " "
        return s
    def get_state(self):
        return [str("gamepad"+str(self.id+1)),str(self.toStr_float()),str(self.toStr_bool())]
    def show_status(self):
        for f in self.get_state():
            padDisplay.arr.append(f)

#padDisplay = TextDisplay("Gamepads")
#padDisplay.updater()

gamepad1 = ol_Gamepad(0)
gamepad2 = ol_Gamepad(1)
gamepad3 = ol_Gamepad(2)
gamepad4 = ol_Gamepad(3)

gamepad1.updater()
gamepad2.updater()
gamepad3.updater()
gamepad4.updater()
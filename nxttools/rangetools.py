# nxttools.rangetools -- module that holds useful functions
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
def clip(VAL,MIN,MAX):
    """VAL is a value that is to be checked
    if the VAL is bigger than MAX, return MAX
    if the VAL is less than MIN, return MIN
    if the VAL is in between MAX and MIN, then return VAL"""
    if(VAL<MIN):
        return MIN
    elif(VAL>MAX):
        return MAX
    elif(isNear(VAL,MIN,0.005)):  #elif(VAL==MIN):
        return MIN
    elif(isNear(VAL,MAX,0.005)):  #elif(VAL==MAX):
        return MAX
    else:
        return round(VAL,2)

def isNear(var,target,threshold):
    """method that returns true if a value is close to
    a target.
    var         is the input number
    target      is the number you want to get near to
    threshold   is how close you want to get to it"""
    diff = var-target
    return abs(diff)<=threshold

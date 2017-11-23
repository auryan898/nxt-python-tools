# nxttools.reactcore -- contains object that can manage and improve efficiency
# of nxt operations
# 
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

class ReactCtl(object):
    CURRSTATE = {} # Holds the values that are used and watched out for
    CURRCOUNT = {}    # Holds the counter that allow values to repeat after 15 counts
    PREVSTATE = CURRSTATE.copy()

    def __init__(self):
        """creates a reactctl object which contains various states inside dictionaries
        useful for telling when a value has changed and then retrieving that same value"""
        pass

    def is_diff(self,ident,initial,newest):
        """returns boolean of whether the values of CURRSTATE and PREVSTATE
        have changed at all at the identity given"""
        if ident not in self.CURRSTATE:
            self.CURRCOUNT[ident] = 0
            self.CURRSTATE[ident] = initial
            self.PREVSTATE[ident] = initial

        # self.CURRSTATE[ident] = newest
        # result = self.CURRSTATE[ident]==self.PREVSTATE[ident]
        # self.PREVSTATE[ident] = self.CURRSTATE[ident]
        # return not result
        return self.update(ident,newest)

    def get_val(self,ident):
        """ident is a String. Gets the current value stored in this object belonging to the
        key of ident."""
        return self.CURRSTATE[ident] if ident in self.CURRSTATE else None
    
    def update(self,ident,value):
        """changes value at identity and increments change counter 
        (tells how many times an ident has been updated)

        returns boolean True if there is a difference between between the new value and the previous value, 
        or if the counter has hit a value divisble by 15. Increments the counter as well."""
        self.CURRSTATE[ident] = value # update current states/values
        isSame = self.CURRSTATE[ident]==self.PREVSTATE[ident] # check if current state is the same as the previous
        self.PREVSTATE[ident] = self.CURRSTATE[ident] # update the previous state for the next check
        self.CURRCOUNT[ident]+=1 # increment the current counter
        if (self.CURRCOUNT[ident]>=150):
            # reset counter if counter is 150
            self.CURRCOUNT[ident]=0
        return (not isSame) or (self.CURRCOUNT[ident]%15 == 0)

reactctl = ReactCtl()
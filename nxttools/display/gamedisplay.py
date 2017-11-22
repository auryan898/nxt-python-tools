# nxttools.gamedisplay -- creates graphics window to display gamepad data
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

# -*- coding: utf-8 -*-
from tkinter import Tk, BOTH
from tkinter.ttk import Frame

class Example(Frame):
  
    def __init__(self):
        super().__init__()
         
        self.initUI()
        
    
    def initUI(self):
      
        self.master.title("Simple")
        self.pack(fill=BOTH, expand=1)
        

def main():
  
    root = Tk()
    root.geometry("250x150+300+300")
    app = Example()
    root.mainloop()  


if __name__ == '__main__':
    main()   
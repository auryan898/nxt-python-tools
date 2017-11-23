# nxttools.sound -- interface to easily control sound on an nxt brick
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


import nxt
note_str = "la la# lb lc lc# ld ld# le lf lf# lg lg# a a# b c c# d d# e f f# g g# ha ha# hb hc hc# hd hd# he hf hf# hg hg# 2a 2a# 2b 2c 2c# 2d 2d# 2e 2f 2f# 2g 2g# 3a 3a# 3b 3c 3c# 3d 3d# 3e 3f 3f# 3g 3g#"
note_arr = note_str.split(" ")
note_freq = {}
def getFreqFunc(x):
    return 220.0*(2.0**(1.0/12.0))**x
for num in range(len(note_arr)):
    note_freq[note_arr[num]] = getFreqFunc(num)



FREQ_E = 659
FREQ_C = 440
play_notes = []

import csv
import time
def csvToSong(filename):
    """batch is a 2d list that contains a list for each note [[le,2,0],[lf#,1,0]]
    may enter batch into playSound() function"""
    f = filename #open(input('Enter file to open') + '.csv','r')
    c = csv.reader(open(f,"r"))
    batch = []
    for row in c:
        batch.append(row)
    #print batch
    return batch
    #    print(row)
import threading
class PlayerObj(threading.Thread):
    FUNC_TYPE = 0
    ARG1 = None
    ARG2 = None
    ARG3 = None
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        if(self.FUNC_TYPE==1):
            self.playSoundSample(self.brick,self.ARG1,self.ARG2)
        if(self.FUNC_TYPE==2):
            self.playSound(self.brick,self.ARG1,self.ARG2)
        if(self.FUNC_TYPE==3):
            self.playNote(self.brick,self.ARG1,self.ARG2,self.ARG3)
        self.FUNC_TYPE = 0
        self.ARG1 = None
        self.ARG2 = None
        self.ARG3 = None

    def safeStart(self):
        if not self.isAlive():
            self.start()
    def playSoundSample(self,b,batchNum,tempo):
        """Plays pre-written songs given a tempo, and a song number (0-6)"""
        def batToString(batch):
            return " ".join( ",".join(x) for x in batch)

        bat = []

        #Mario!!!
        bat.append("e,1,1 e,1,1 e,3,0 c,1,0 e,2,0 g,1,2 lg,3,0")
        #That Rally Call tune
        bat.append("d,1,1 d,2,0 f#,2,0 ha,3,0 f#,1,0 ha,3,0")
        #the Windows I Screwed Up noise
        bat.append("lb,1,1 lb,2,0")
        #Sad noise when mistakes are made
        bat.append("g,1,0 f#,1,0 f,1,0 e,3,0")
        #mario got a coin noise
        bat.append("b,1,0 d,1,0 c,1,0 e,1,0")
        bat.append("a,1,0 c,1,0 e,1,0 ha,1,0")
        #question noise
        bat.append("a,1,0 f,1,0 e,1,0")

        batchArr = [arr.split(",") for arr in bat[batchNum].split(" ")]

        # A F# E
        # B D C E
        # A C E hA
        self.playSound(b,batchArr,tempo)
    def playSound(self,b,batch,tempo):
        """tempo is a BPM number for the song
        batch is a 2d list that contains a list for each note [["le",2,0],["lf"#,1,0]]
        [[note name, duration, amount of silence after]]"""
        #f = open(input('Enter file to open') + '.csv','r')
        #c = csv.reader(f)
        #batch = []
        #for row in c:
        #    batch.append(row)
        #    print(row)
        raw = []
        for item in batch:
            raw.append([note_freq[item[0]],item[1],item[2]])

        #tempo = 120#int(input('What tempo do you want to play this as in BPM'))
        cor_tempo = (1000/(tempo/60))/4
        #print('Milliseconds per semi-quaver is:' + str(cor_tempo))
        for item in raw:
            #print(item)
            b.play_tone_and_wait(int(item[0]), int(item[1]) * int(cor_tempo))
            time.sleep(float(item[2]) * cor_tempo/1000)
    def playNote(self,b,name,duration=1,variance=0):
        """name from the note_freq dictionary, duration is in Milliseconds
        variance is percentage pitch modulation from given to tone to next tones
            ex. 0.5 to next halfstep, 1 to next wholestep, negative for lower pitch"""
        freq = note_freq[name]*(2.0**(1.0/12.0))**(variance*2)
        b.play_tone(int(freq),duration)

#SoundBrick.playSound(csvToSong("victory"),120)
import random
class Player(object):
    def __init__(self,brick):
        self.obj = PlayerObj()
        self.brick = brick
    def playSoundSample(self,batchNum,tempo):
        """Plays pre-written songs given a tempo, and a song number (0-6)"""
        self.safeCreation()
        self.obj.brick = self.brick
        self.obj.FUNC_TYPE = 1
        self.obj.ARG1 = batchNum
        self.obj.ARG2 = tempo
        self.obj.safeStart()
    def playSound(self,batch,tempo):
        """tempo is a BPM number for the song
        batch is a 2d list that contains a list for each note [["le",2,0],["lf"#,1,0]]
        [[note name, duration, amount of silence after]]"""
        self.safeCreation()
        self.obj.brick = self.brick
        self.obj.FUNC_TYPE = 2
        self.obj.ARG1 = batch
        self.obj.ARG2 = tempo
        self.obj.safeStart()
    def playNote(self,noteName,duration,variance):
        """name from the note_freq dictionary, duration is in Milliseconds
        variance is percentage pitch modulation from given to tone to next tones
            ex. 0.5 to next halfstep, 1 to next wholestep, negative for lower pitch"""
        self.safeCreation()
        self.obj.brick = self.brick
        self.obj.FUNC_TYPE = 3
        self.obj.ARG1 = noteName
        self.obj.ARG2 = duration
        self.obj.ARG3 = variance
        self.obj.safeStart()
    def safeCreation(self):
        if not self.obj.isAlive():
            self.obj = PlayerObj()
    def success(self):
        """displays a random success message and plays a sound sample 1"""
        message = [
        "It is fully operational!",
        "It's alive!",
        "Houston we are a go.",
        "Cue the music.",
        "Let's roll out!"
        ]
        print message[random.randint(0,len(message)-1)]
        self.playSoundSample(1,120)
    def playFile(self,filename,tempo):
        """accepts a string filename and an integer tempo. plays song based on contents of file 
        according to preset template.

        A single line of the csv file representing a note is setup as follows:
        letter_name,play_time(sixteenth notes),wait_time(sixteenth notes)

        For letter_name there are no flats, but there are sharps:
            la    a    ha    2a    3a
        The la (low A note) is the lowest note possible. 
        The 3g# is the highest note programmed (but may not play).
        """
        self.playSound(csvToSong(csvfilename),tempo)
    def csvToSong(filename):
        """batch is a 2d list that contains a list for each note [[le,2,0],[lf#,1,0]]
        may enter batch into playSound() function"""
        f = filename #open(input('Enter file to open') + '.csv','r')
        c = csv.reader(open(f,"r"))
        batch = []
        for row in c:
            batch.append(row)
        #print batch
        return batch
        #    print(row)

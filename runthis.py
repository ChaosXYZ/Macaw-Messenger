#!/usr/bin/python
# -*- coding: utf-8 -*-
# Title: Macaw Massacre, Author: Alan Vincent
# ID: 10456956
#
# Image sources
# background.png. night.png - https://opengameart.org/collections
# toucan and macaw:
# https://opengameart.org/content/opp2017-sprites-characters-objects-effects
# Button images and instructions:
# https://cooltext.com/
# https://pixlr.com/
from tkinter import *
import random
import threading
import time
# Setting the dimensions and importing variables
world = Tk()
world.title('Macaw Massacre')
world.geometry('800x480')
global bg1, lbd, direction, work, music, toucan, heart
music = True
work = PhotoImage(file='work.png')
bg1 = PhotoImage(file='background.png')
heart = PhotoImage(file='heart.png')
lbd = [0, 0, 0, 0, 0]

# Clears a canvas
def clear(x):
    x.pack_forget()

# Displats the leaderboard
def lbscreen():

    def l2mt():
        clear(leader)
        main()

    global bg1
    clear(jungle)
    leader = Canvas(world, width=200, height=100, bg='white')
    leader.pack(fill=BOTH, expand=YES)
    leader.create_image(0, 0, image=bg1, anchor='nw')
    content = Label(leader,
                    text='''Leaderboard (Non-Retro Anonymous Style)


                    1.{}


                    2.{}


                    3.{}


                    4.{}


                    5.{}'''.format(lbd[0],
                                   lbd[1], lbd[2], lbd[3], lbd[4]), width='40',
                    height='20',
                    bg='#82BF43').place(x=250, y=80)
    back = Button(leader, text='Go Back', command=lambda:
                  l2mt()).place(x=623, y=380)

# Recursively updates the leaderboard
def updatelb(score):
    flipped = False
    for i in range(0, 5):
        if score > lbd[i]:
            templbd = lbd[i]
            lbd[i] = score
            updatelb(templbd)
            break
    tempfile = open('data.txt', 'w+')
    for i in range(0, 5):
        tempfile.write(str(lbd[i]) + '\n')
    tempfile.close()

# Saves the leaderboard into a file to be imported later
def savelb(lebd):

    def s2mt():
        clear(saver)
        main()

    global bg1
    clear(jungle)
    saver = Canvas(world, width=200, height=100, bg='white')
    saver.pack(fill=BOTH, expand=YES)
    saver.create_image(0, 0, image=bg1, anchor='nw')
    save = random.randint(1000000, 9999999)
    tempfile = open('SAV' + str(save) + '.txt', 'w+')
    for i in range(0, 5):
        tempfile.write(str(lebd[i]) + '\n')
    tempfile.close()
    savename = \
        '''The contents of the leaderboard have been saved into a file:

File saved to SAV''' \
        + str(save) + '.txt'
    savenamelabel = Label(saver, text=savename, bg='#82BF43'
                          ).place(x=250, y=180)
    back = Button(saver, text='Go Back', command=lambda:
                  s2mt()).place(x=623, y=380)

# The main gameplay functionality
def playbtn():
    global animator, paused, score, shot, playgame, toucanalive, shot, \
        lives, heartexists, wasdvar
    toucanalive = False
    heartexists = False
    paused = False
    animator = 0
# The Animate function will be run parallel to all the other functions
# it handles macaw animation, toucan and heart generation
    def Animate():
        global toucan, shot, playgame, sy1, sy2, heart, tposy, tposx, \
            hposx, hposy
        (tposy, tposx, hposx, hposy) = (0, 0, 0, 0)
        (sy1, sy2) = (0, 0)
        if not paused:
            global animator, score, toucanalive, heartexists
            animator = 0
            while True:
                playgame.delete(shot)
                if not paused:
                    score += 1
                    scoredisplay.config(text='Score: ' + str(score))
                    if score % 10 == 0 and not toucanalive:
                        generatorkey = random.randint(1, 10)
                        if generatorkey > 4:
                            toucansprite = PhotoImage(file='toucan.gif')
                            toucan = Label(playgame, text='',
                                           image=toucansprite)
                            toucan.image = toucansprite
                            tposx = 700
                            tposy = random.randint(0, 400)
                            toucan.place(x=tposx, y=tposy)
                            toucanalive = True
                    if toucanalive:
                        if int((sy1 + sy2) / 2) in range(tposy + 5,
                                                         tposy + 70):
                            toucan.destroy()
                            score += 750
                            toucanalive = False
                        if tposx <= 20 and toucanalive:
                            toucan.destroy()
                            toucanalive = False
                            global lives
                            lives -= 1
                            lifedisplay.config(text='Lives: ' + str(lives))
                            deathcheck()
                        elif tposx > 20 and toucanalive:
                            if not paused:
                                flyspeed = int(score / 1000) + 7
                                if flyspeed > 55:
                                    tposx -= 55
                                else:
                                    tposx -= flyspeed
                                toucan.place(x=tposx, y=tposy)
                    global heartexists
                    if score > 10000 and not heartexists:
                        genkey = random.randint(1, 1000)
                        if genkey > 998:
                            heartsprite = PhotoImage(file='heart.png')
                            heart = Label(playgame, text='',
                                          image=heartsprite)
                            heart.image = heartsprite
                            hposx = 700
                            hposy = random.randint(0, 400)
                            heart.place(x=hposx, y=hposy)
                            heartexists = True
                    if heartexists:
                        if int((sy1 + sy2) / 2) in range(hposy + 5,
                                                         hposy + 70):
                            heart.destroy()
                            lives += 1
                            lifedisplay.config(text='Lives: ' + str(lives))
                            heartexists = False
                        if hposx <= 20 and heartexists:
                            heart.destroy()
                            heartexists = False
                        elif hposx > 20 and heartexists:
                            if not paused:
                                hposx -= 25
                                heart.place(x=hposx, y=hposy)
                time.sleep(.100)
                #the animator function loops through images to animate the
                #bird
                if animator > 1000:
                    animator = 0
                else:
                    animator += 1
                spritesheet = [
                    'macaw.png',
                    'macaw2.png',
                    'macaw3.png',
                    'macaw4.png',
                    'macaw5.png',
                    'macaw6.png',
                    'macaw7.png',
                    'macaw8.png',
                    ]
                macawsprite = PhotoImage(file='macaw.png')
                macawsprite1 = PhotoImage(file='macaw1.png')
                macawsprite2 = PhotoImage(file='macaw2.png')
                macawsprite3 = PhotoImage(file='macaw3.png')
                macawsprite4 = PhotoImage(file='macaw4.png')
                macawsprite5 = PhotoImage(file='macaw5.png')
                macawsprite6 = PhotoImage(file='macaw6.png')
                macawsprite7 = PhotoImage(file='macaw7.png')
                macawsprite8 = PhotoImage(file='macaw8.png')
                if animator % 9 == 0:
                    macaw.config(image=macawsprite)
                    macaw.image = macawsprite
                elif animator % 9 == 1:
                    macaw.config(image=macawsprite1)
                    macaw.image = macawsprite1
                elif animator % 9 == 2:
                    macaw.config(image=macawsprite2)
                    macaw.image = macawsprite2
                elif animator % 9 == 3:
                    macaw.config(image=macawsprite3)
                    macaw.image = macawsprite3
                elif animator % 9 == 4:
                    macaw.config(image=macawsprite4)
                    macaw.image = macawsprite4
                elif animator % 9 == 5:
                    macaw.config(image=macawsprite5)
                    macaw.image = macawsprite5
                elif animator % 9 == 6:
                    macaw.config(image=macawsprite6)
                    macaw.image = macawsprite6
                elif animator % 9 == 7:
                    macaw.config(image=macawsprite7)
                    macaw.image = macawsprite7
                elif animator % 9 == 8:
                    macaw.config(image=macawsprite8)
                    macaw.image = macawsprite8

    def upKey(*args):
        global y1
        if y1 < -5:
            y1 = -5
        else:
            y1 += -5
        macaw.place(x=x1, y=y1)

    def downKey(*args):
        global y1
        if y1 > 415:
            y1 = 415
        else:
            y1 += 5
        macaw.place(x=x1, y=y1)
 #functions for the cheatcodes
    def scorecheat(*args):
        global score
        score += 10000
        scoredisplay.config(text='Score: ' + str(score))

    def lifecheat(*args):
        global lives
        lives += 1
        lifedisplay.config(text='Lives: ' + str(lives))
 #saves the current state of the game, ignoring toucans to prevent abuse
    def savestate():
        global lives, score, x1, y1
        statefile = open('game.txt', 'w+')
        statefile.write(str(lives) + '\n')
        statefile.write(str(score) + '\n')
        statefile.write(str(x1) + '\n')
        statefile.write(str(y1) + '\n')
        statefile.close()

    def loadstate():
        global lives, score, x1, y1
        statelist = [line.rstrip('\n') for line in open('game.txt')]
        if len(statelist) > 3:
            try:
                lives = int(statelist[0])
                score = int(statelist[1])
                x1 = int(statelist[2])
                y1 = int(statelist[3])
                scoredisplay.config(text='Score: ' + str(score))
                lifedisplay.config(text='Lives: ' + str(lives))
                macaw.move(x1, y1)
            except:
                pass
 #Laser shooting function, generates a rectangle
    def shoot(*args):
        global x1, y1, shot, sy1, sy2
        playgame.delete(shot)
        (sy1, sy2) = (y1 + 30, y1 + 35)
        shot = playgame.create_rectangle(x1 + 70, sy1, x1 + 775, sy2,
                                         fill='red')
 #glorified pause button
    def bosskey(*args):
        global paused, bosskey, score, lives
        if not paused:
            bosskey = Canvas(playgame, width=20, height=100, bg='white')
            bosskey.pack(fill=BOTH, expand=YES)
            bosskey.create_image(0, 0, image=work, anchor='nw')
            world.title('Budget Analysis 2.0')
            try:
                if wasdvar.get():
                    playgame.unbind('w')
                    playgame.unbind('s')
                elif not wasdvar.get():
                    playgame.unbind('<Up>')
                    playgame.unbind('<Down>')
            except:
                playgame.unbind('<Up>')
                playgame.unbind('<Down>')
            playgame.unbind('<space>')
            paused = True
        else:
            try:
                if wasdvar.get():
                    playgame.bind('<w>', upKey)
                    playgame.bind('<s>', downKey)
                elif not wasdvar.get():
                    playgame.bind('<Up>', upKey)
                    playgame.bind('<Down>', downKey)
            except:
                playgame.bind('<Up>', upKey)
                playgame.bind('<Down>', downKey)
            playgame.bind('<space>', shoot)
            world.title('Macaw Massacre')
            clear(bosskey)
            paused = False
 #changes the global paused variable which signals to the Animation thread
 #to stop running, acting as a pseudo-flag for it.
    def pausekey(*args):

        def p2mt():
            global toucanalive
            toucanalive = False
            clear(playgame)
            clear(bosskey)
            main()

        global paused, bosskey, score, lives, bg1
        if not paused:
            bosskey = Canvas(playgame, width=20, height=100, bg='white')
            bosskey.pack(fill=BOTH, expand=YES)
            bosskey.create_image(0, 0, image=bg1, anchor='nw')
            info1 = Label(bosskey, text='GAME PAUSED', fg='red',
                          font=('Courier', 44)).place(x=200, y=120)
            info2 = Label(bosskey, text='Press P to unpause',
                          font=('Courier', 35)).place(x=135, y=200)
            info3 = Label(bosskey,
                          text="""Cheatcodes:
'scorezz' grants +10000 score.
'heartz' grants a life.""",
                          font=('Courier', 30)).place(x=35, y=280)
            mm = Button(bosskey, text='Main Menu', command=lambda:
                        p2mt()).place(x=350, y=435)

            try:
                if wasdvar.get():
                    playgame.unbind('w')
                    playgame.unbind('s')
                elif not wasdvar.get():
                    playgame.unbind('<Up>')
                    playgame.unbind('<Down>')
            except:
                playgame.unbind('<Up>')
                playgame.unbind('<Down>')
            playgame.unbind('<space>')
            paused = True
        else:
            try:
                if wasdvar.get():
                    playgame.bind('<w>', upKey)
                    playgame.bind('<s>', downKey)
                elif not wasdvar.get():
                    playgame.bind('<Up>', upKey)
                    playgame.bind('<Down>', downKey)
            except:
                playgame.bind('<Up>', upKey)
                playgame.bind('<Down>', downKey)
            playgame.bind('<space>', shoot)
            clear(bosskey)
            paused = False
 #Handles all death
    def deathcheck(*args):
        global lives
        lifedisplay.config(text='Lives: ' + str(lives))

        def d2mt():
            clear(death)
            main()

        if lives == 0:
            toucanalive = False
            clear(playgame)
            death = Canvas(world, width=200, height=100, bg='white')
            death.pack(fill=BOTH, expand=YES)
            death.create_image(0, 0, image=bg1, anchor='nw')
            gameover = PhotoImage(file='gameover.png')
            gameoverlabel = Label(death, text='', image=gameover)
            gameoverlabel.image = gameover
            gameoverlabel.place(x=200, y=40)
            updatelb(score)
            gamescore = 'Your score is: ' + str(score)
            gamescorelabel = Label(death, text=gamescore).place(x=375,
                                                                y=300)
            back = Button(death, text='Main Menu', command=lambda:
                          d2mt()).place(x=380, y=400)

    clear(jungle)
    global score, lives, x1, y1

    (score, lives, x1, y1) = (0, 3, 20, 10)
    playgame = Canvas(world, width=200, height=100, bg='white')
    shot = playgame.create_rectangle(0, 0, 0, 0, fill='red')
    playgame.pack(fill=BOTH, expand=YES)
    playgame.create_image(0, 0, image=bg1, anchor='nw')

    scoredisplay = Label(playgame, text='Score: ' + str(score))
    scoredisplay.place(x=710, y=10)
    lifedisplay = Label(playgame, text='Lives: ' + str(lives))
    lifedisplay.place(x=660, y=10)
    try:
        if wasdvar.get():
            playgame.bind('<w>', upKey)
            playgame.bind('<s>', downKey)
        elif not wasdvar.get():
            playgame.bind('<Up>', upKey)
            playgame.bind('<Down>', downKey)
    except:
        playgame.bind('<Up>', upKey)
        playgame.bind('<Down>', downKey)
    playgame.bind('<space>', shoot)
    playgame.bind('<p>', pausekey)
    playgame.bind('<s><c><o><r><e><z><z>', scorecheat)
    playgame.bind('<h><e><a><r><t><z>', lifecheat)
    playgame.bind('<b>', bosskey)
    playgame.focus_set()
    macawsprite = PhotoImage(file='macaw.png')
    macaw = Label(playgame, text='', image=macawsprite)
    macaw.image = macawsprite
    macaw.place(x=x1, y=y1)
    sstate = Button(playgame, text='Save', command=lambda:
                    savestate()).place(x=550, y=10)
    lstate = Button(playgame, text='Load', command=lambda:
                    loadstate()).place(x=500, y=10)
    thread = threading.Thread(target=Animate)
    thread.start()

# Instructions window

def instructions():

    def i2mt():
        clear(instruct)
        main()

    clear(jungle)
    instruct = Canvas(world, width=200, height=100, bg='white')
    instruct.pack(fill=BOTH, expand=YES)
    instruct.create_image(0, 0, image=bg1, anchor='nw')
    instructimg = PhotoImage(file='instructions.png')
    bg123 = '#82BF43'
    ins = Label(instruct, text='', image=instructimg, height='480', bg=bg123)
    ins.image = instructimg
    ins.place(x=0, y=0)
    back = Button(instruct, text='Main Menu', command=lambda:
                  i2mt()).place(x=700, y=450)

# Attempts to load custom leaderboard, if not found it will just display error

def loadGUI():
    global music

    def load2mt():
        clear(lbloader)
        main()

    def fileload():
        try:
            savfile = lbfilename.get()
            lineList = [line.rstrip('\n') for line in open(savfile)]
            for i in range(0, 5):
                lbd[i] = int(lineList[i])
            loadstatus.config(text='Success!')
            loadstatus.config(fg='green')
        except:
            temptext1 = 'Unsuccessful! Did you remember to add .txt?'
            loadstatus.config(text=temptext1)
            loadstatus.config(fg='red')

    clear(jungle)
    lbloader = Canvas(world, width=200, height=100, bg='white')
    lbloader.pack(fill=BOTH, expand=YES)
    lbloader.create_image(0, 0, image=bg1, anchor='nw')
    lbtext = lbloader.create_text(410, 130,
                                  text='Enter leaderboard filename to load: '
                                  )
    lbfilename = Entry(lbloader)
    lbfilename.place(x=350, y=150)
    back = Button(lbloader, text='Go Back', command=lambda:
                  load2mt()).place(x=480, y=200)
    load = Button(lbloader, text='Load', command=lambda:
                  fileload()).place(x=300, y=200)
    loadstatus = Label(lbloader, text='', fg='white')
    loadstatus.place(x=470, y=150)

# Controls WASD and night mode

def settings():

    def apply():
        global musicvar, music, bg1
        if not backvar.get():
            bg1 = PhotoImage(file='background.png')
        elif backvar.get():
            bg1 = PhotoImage(file='night.png')
        clear(settings)
        main()

    clear(jungle)
    settings = Canvas(world, width=200, height=100, bg='white')
    settings.pack(fill=BOTH, expand=YES)
    settings.create_image(0, 0, image=bg1, anchor='nw')
    global musicvar, backvar, wasdvar
    wasdvar = BooleanVar()
    backvar = BooleanVar()
    wasdbox = Checkbutton(settings, text='Use WASD', var=wasdvar,
                          onvalue=True, offvalue=False).place(x=100,
                                                              y=100)
    backbox = Checkbutton(settings, text='Night mode', var=backvar,
                          onvalue=True, offvalue=False).place(x=300,
                                                              y=100)
    back = Button(settings, text='Apply and save', command=lambda:
                  apply()).place(x=350, y=50)


def main():
    global jungle, bg1, music
    jungle = Canvas(world, width=200, height=100, bg='white')
    jungle.pack(fill=BOTH, expand=YES)

    # Background

    jungle.create_image(0, 0, image=bg1, anchor='nw')
    logo = PhotoImage(file='logo.png')
    jungle.create_image(85, 0, image=logo, anchor='nw')

    # loadleaderboard

    lineList = [line.rstrip('\n') for line in open('data.txt')]
    for i in range(0, 5):
        lbd[i] = int(lineList[i])

    # Buttons

    Playbutton = PhotoImage(file='Play.png')
    play = Button(jungle, text='OK', command=lambda: playbtn(),
                  image=Playbutton).place(x=20, y=270)
    leaderbutton = PhotoImage(file='Leaderboard.png')
    leader = Button(jungle, text='OK', command=lambda: lbscreen(),
                    image=leaderbutton).place(x=240, y=270)
    Savebutton = PhotoImage(file='Save.png')
    save = Button(jungle, text='OK', command=lambda: savelb(lbd),
                  image=Savebutton).place(x=520, y=390)
    Loadbutton = PhotoImage(file='Load.png')
    load = Button(jungle, text='OK', command=lambda: loadGUI(),
                  image=Loadbutton).place(x=643, y=390)
    Settingsbutton = PhotoImage(file='setting.png')
    setting = Button(jungle, text='OK', command=lambda: settings(),
                     image=Settingsbutton).place(x=20, y=180)
    insimg = PhotoImage(file='insbutton.png')
    insbutton = Button(jungle, text='OK', command=lambda:
                       instructions(), image=insimg).place(x=230, y=390)
    world.mainloop()


main()

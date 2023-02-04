import tkinter.ttk
from tkinter import *

from PIL import ImageTk, Image, ImageFile

import os
import threading

from helpers import guiHelper

import common
import twitchModule as tm
import backendLogic as backend


root = None
getPuzzlesButton = None
leftFrame, scoreboardFrame, patronsFrame, puzzleFrame, vsInfoFrame, configureFrame, puzzleInfoFrame = None, None, None, None, None, None, None
issueLabel, puzzleImageLabel, ratingLabel, themeLabel, gameUrlLabel = None, None, None, None, None

pb = None

scoreboardItems = []
patronsAllFrames = []
mode = 2


def fillAndDisplayPatronsFrame():
    global patronsAllFrames

    for f in patronsAllFrames:
        f.destroy()

    for count, patron in enumerate(tm.subsAndStatus):
        if count % 2 == 0:
            frame = guiHelper.FrameOfPacksPackPlacement(patronsFrame, (300, 40), TOP, guiHelper.LICHESSBGLIGHT)
            if patron[0] == "nimoniktr":
                guiHelper.ImageOnFramePackPlacement(frame, "images/patronBoss.png", (20, 20), guiHelper.LICHESSBGLIGHT, LEFT)
            else:
                if patron[1]:
                    guiHelper.ImageOnFramePackPlacement(frame, "images/patronOnline.png", (20, 20), guiHelper.LICHESSBGLIGHT,
                                                        LEFT)
                else:
                    guiHelper.ImageOnFramePackPlacement(frame, "images/patron.png", (20, 20), guiHelper.LICHESSBGLIGHT, LEFT)

            guiHelper.LabelPackPlacement(frame, patron[0], guiHelper.LICHESSBGLIGHT, guiHelper.FGWHITE, ('Lucida Console', 13),
                                         LEFT)
        else:
            frame = guiHelper.FrameOfPacksPackPlacement(patronsFrame, (300, 40), TOP, guiHelper.LICHESSBGDARK)
            if patron[0] == "nimoniktr":
                guiHelper.ImageOnFramePackPlacement(frame, "images/patronBoss.png", (20, 20), guiHelper.LICHESSBGDARK, LEFT)
            else:
                if patron[1]:
                    guiHelper.ImageOnFramePackPlacement(frame, "images/patronOnline.png", (20, 20), guiHelper.LICHESSBGDARK,
                                                        LEFT)
                else:
                    guiHelper.ImageOnFramePackPlacement(frame, "images/patron.png", (20, 20), guiHelper.LICHESSBGDARK, LEFT)

            guiHelper.LabelPackPlacement(frame, patron[0], guiHelper.LICHESSBGDARK, guiHelper.FGWHITE, ('Lucida Console', 13), LEFT)
        patronsAllFrames.append(frame)


def createNewScoreboardItem(key_value, even):
    print("createNewScoreboardItem start:", key_value)
    bg = "#262421" if even else "#302E2C"

    nameTxt = str(key_value[0])
    ratingTxt = str(int(key_value[1][2].mu))

    newFrame = guiHelper.FrameOfPacksPackPlacement(scoreboardFrame, (300, 40), TOP, bg)

    # if user sub
    if key_value[1] and nameTxt != "nimoniktr":
        # isSubOnline = False
        for e in tm.subsAndStatus:
            if nameTxt == e[0]:
                isSubOnline = e[1]
        if isSubOnline:
            guiHelper.ImageOnFramePackPlacement(newFrame, "images/patronOnline.png", (20, 20), bg, LEFT)
            guiHelper.LabelPackPlacement(newFrame, nameTxt, bg, guiHelper.FGWHITE, ('Lucida Console', 13), LEFT)
            guiHelper.LabelPackPlacement(newFrame, ratingTxt, bg, guiHelper.FGWHITE, ('Lucida Console', 13), RIGHT)
            print("Frame object created using patronOnline.png")
        else:
            guiHelper.ImageOnFramePackPlacement(newFrame, "images/patron.png", (20, 20), bg, LEFT)
            guiHelper.LabelPackPlacement(newFrame, nameTxt, bg, guiHelper.FGWHITE, ('Lucida Console', 13), LEFT)
            guiHelper.LabelPackPlacement(newFrame, ratingTxt, bg, guiHelper.FGWHITE, ('Lucida Console', 13), RIGHT)
            print("Frame object created using patron.png")
    elif nameTxt == "nimoniktr":
        guiHelper.ImageOnFramePackPlacement(newFrame, "images/patronBoss.png", (20, 20), bg, LEFT)
        guiHelper.LabelPackPlacement(newFrame, nameTxt, bg, guiHelper.FGWHITE, ('Lucida Console', 13), LEFT)
        guiHelper.LabelPackPlacement(newFrame, ratingTxt, bg, guiHelper.FGWHITE, ('Lucida Console', 13), RIGHT)
        print("Frame object created using patronBoss.png")
    else:
        guiHelper.ImageOnFramePackPlacement(newFrame, "images/online.png", (20, 20), bg, LEFT)
        guiHelper.LabelPackPlacement(newFrame, nameTxt, bg, guiHelper.FGWHITE, ('Lucida Console', 13), LEFT)
        guiHelper.LabelPackPlacement(newFrame, ratingTxt, bg, guiHelper.FGWHITE, ('Lucida Console', 13), RIGHT)
        print("Frame object created using online.png")

    print("createNewScoreboardItem end:", key_value)

    return newFrame


def destroyItems():
    for e in scoreboardItems:
        e.destroy()


def on_enter(btn):
    if btn is not None and btn['state'] == "normal":
        btn['fg'] = "white"


def on_leave(btn):
    if btn is not None and btn['state'] == "normal":
        btn['fg'] = "#999999"


def placePuzzleImage(imgFile, isLastMove=False):
    global puzzleImageLabel
    if puzzleImageLabel is not None:
        puzzleImageLabel.destroy()
    if not isLastMove:
        img = Image.open(imgFile)

        # Create a photoimage object of the image in the path
        test = ImageTk.PhotoImage(img.resize((500, 500)))

        puzzleImageLabel = Label(puzzleFrame, width=600, height=600, image=test, bg="#262421")
        puzzleImageLabel.image = test

        # Position image
        puzzleImageLabel.pack()
    else:
        img = Image.open("images/solved.png")

        background = Image.open(imgFile)

        background.paste(img, (0, 0), img)
        background.save('NewImg.png', "PNG")

        NewImg = Image.open('NewImg.png')

        # Use Image
        test = ImageTk.PhotoImage(NewImg.resize((500, 500)))

        puzzleImageLabel = Label(puzzleFrame, width=600, height=600, image=test, bg="#262421")
        puzzleImageLabel.image = test

        # Position image
        puzzleImageLabel.pack()


def showPuzzleInfo(data):
    global ratingLabel, popularityLabel, themeLabel, gameUrlLabel

    backend.puzzleRating = data[0]
    ratingLabel = Label(puzzleInfoFrame, text=f"\n{backend.puzzleRating}", bg="#262421", font=("Roboto", 18), fg="#BABAAB")
    ratingLabel.pack()


def deletePuzzleInfo():
    if ratingLabel is not None:
        ratingLabel.destroy()
    if themeLabel is not None:
        themeLabel.destroy()
    if gameUrlLabel is not None:
        gameUrlLabel.destroy()
    issueLabel.config(text="")


def showProgressbar():
    global pb

    s = tkinter.ttk.Style()
    s.theme_use('clam')
    s.configure("red.Horizontal.TProgressbar", foreground="#B47A1D", background="white")

    pb = tkinter.ttk.Progressbar(configureFrame, style="red.Horizontal.TProgressbar", mode='indeterminate', length=200)
    pb.start()
    pb.pack(side=BOTTOM)


def deleteProgressbar():
    pb.destroy()


def startReading():
    deletePuzzleInfo()
    getPuzzlesButton["state"] = "disabled"
    showProgressbar()


def stopReading():
    getPuzzlesButton["state"] = "normal"
    deleteProgressbar()


def onExceptionOccured():

    backend.puzzleAnswer = None
    issueLabel.config(text="Corrupted database try again!")
    getPuzzlesButton["state"] = "normal"


def onClickGetPuzzles():
    backend.puzzleAnswer = None

    t = threading.Thread(
        target=lambda: common.getPuzzles(mode))
    t.start()


def onExit():
    print("onExit start:")
    backend.saveRatingsToDatabaseFile()
    for fname in os.listdir(os.getcwd()):
        if fname.startswith("pos") or fname.startswith("outputpos"):
            os.remove(fname)
    root.destroy()
    print("onExit end:")


def startGui():
    global root, nextBtn, revealBtn, puzzleFrame, \
        vsInfoFrame, issueLabel, leftFrame, \
        generateButton, configureFrame, scoreboardFrame, puzzleInfoFrame, getPuzzlesButton, patronsFrame

    #################################################################################################################################################

    root = guiHelper.RootWindowOfGrids("Lichess-Twitch Puzzle", "1550x800", guiHelper.LICHESSBGDARKMAIN)

    ##################################################################################################################################################

    mainFrame = guiHelper.FrameOfGridsGridPlacement(root, (600, 700), (0, 1), guiHelper.LICHESSBGLIGHT)
    guiHelper.DummyFrameGridPlacement(mainFrame, (600, 25), (0, 0), guiHelper.LICHESSBGLIGHT)
    puzzleFrame = guiHelper.FrameOfPacksGridPlacement(mainFrame, (600, 575), (1, 0), guiHelper.LICHESSBGLIGHT)
    vsInfoFrame = guiHelper.FrameOfGridsGridPlacement(mainFrame, (600, 100), (2, 0), guiHelper.LICHESSBGLIGHT)

    ###################################################################################################################################################

    leftFrame = guiHelper.FrameOfGridsGridPlacement(root, (200, 700), (0, 0), guiHelper.LICHESSBGDARKMAIN, 30, 10)

    guiHelper.DummyFrameGridPlacement(leftFrame, (200, 50), (0, 0), guiHelper.LICHESSBGDARKMAIN)

    logoFrame = guiHelper.FrameOfPacksGridPlacement(leftFrame, (200, 100), (1, 0), guiHelper.LICHESSBGDARKMAIN)
    guiHelper.ImageOnFramePackPlacement(logoFrame, "images/Lichess_logo_2019.png", (100, 100), guiHelper.LICHESSBGDARKMAIN)

    lichessOrgFrame = guiHelper.FrameOfPacksGridPlacement(leftFrame, (200, 100), (2, 0), guiHelper.LICHESSBGDARKMAIN)
    guiHelper.LabelPackPlacement(lichessOrgFrame, "lichess.org", guiHelper.LICHESSBGDARKMAIN, guiHelper.FGGRAY, guiHelper.FONT15, TOP,
                                 pady=10)

    streamerWingFrame = guiHelper.FrameOfPacksGridPlacement(leftFrame, (200, 100), (3, 0), guiHelper.LICHESSBGDARKMAIN)
    guiHelper.ImageOnFramePackPlacement(streamerWingFrame, "images/WingFlame.png", (50, 50), guiHelper.LICHESSBGDARKMAIN, TOP)
    guiHelper.LabelPackPlacement(streamerWingFrame, "Nimoniktr", guiHelper.LICHESSBGDARKMAIN, guiHelper.FGWHITE, guiHelper.FONT15,
                                 BOTTOM)

    puzzleInfoFrame = guiHelper.FrameOfPacksGridPlacement(leftFrame, (200, 80), (4, 0), guiHelper.LICHESSBGLIGHT, pady=20)

    def flt():
        global mode
        mode = var.get()

    var = IntVar(None, 2)

    s = tkinter.ttk.Style()  # Creating style element
    s.configure('Wild.TRadiobutton',  # First argument is the name of style. Needs to end with: .TRadiobutton
                background=guiHelper.LICHESSBGLIGHT,  # Setting background to our specified color above
                foreground=guiHelper.LICHESSGOLD)  # You can define colors like this also
    s2 = tkinter.ttk.Style()  # Creating style element
    s2.configure('Dark.TRadiobutton',  # First argument is the name of style. Needs to end with: .TRadiobutton
                 background=guiHelper.LICHESSBGDARK,  # Setting background to our specified color above
                 foreground=guiHelper.LICHESSGOLD)  # You can define colors like this also

    R1 = tkinter.ttk.Radiobutton(leftFrame, text="Easy", variable=var, value=1, command=flt, style='Wild.TRadiobutton',
                                 width=30)
    R1.grid(row=5, column=0)
    R2 = tkinter.ttk.Radiobutton(leftFrame, text="Medium", variable=var, value=2, command=flt,
                                 style='Dark.TRadiobutton', width=30)
    R2.grid(row=6, column=0)
    R3 = tkinter.ttk.Radiobutton(leftFrame, text="Hard", variable=var, value=3, command=flt, style='Wild.TRadiobutton',
                                 width=30)
    R3.grid(row=7, column=0)

    guiHelper.DummyFrameGridPlacement(leftFrame, (200, 50), (8, 0), guiHelper.LICHESSBGDARKMAIN)

    configureFrame = guiHelper.FrameOfPacksGridPlacement(leftFrame, (200, 100), (9, 0), guiHelper.LICHESSBGLIGHT)
    getPuzzlesButton = Button(configureFrame, text="SEARCH", command=onClickGetPuzzles,
                              width=30, height=3, bg="#373531", fg="#999999", borderwidth=0, highlightthickness=0,
                              activebackground="#de5100", disabledforeground="black")
    getPuzzlesButton.bind("<Enter>", lambda event: on_enter(getPuzzlesButton))
    getPuzzlesButton.bind("<Leave>", lambda event: on_leave(getPuzzlesButton))
    getPuzzlesButton.pack(side=TOP)

    issueLabel = guiHelper.LabelPackPlacement(configureFrame, "", guiHelper.LICHESSBGLIGHT, guiHelper.FGWHITE, guiHelper.FONT10, BOTTOM,
                                              width=200, height=2)

    ######################################################################################################################################################

    scoreboardFrame = guiHelper.FrameOfPacksGridPlacement(root, (300, 700), (0, 2), guiHelper.LICHESSBGDARKMAIN, 30)
    guiHelper.LabelPackPlacement(scoreboardFrame, 'Puzzle Top 10', guiHelper.LICHESSBGLIGHT, guiHelper.FGGRAY, guiHelper.FONT15, TOP,
                                 width=300, height=3)

    ######################################################################################################################################################
    patronsFrame = guiHelper.FrameOfPacksGridPlacement(root, (300, 700), (0, 3), guiHelper.LICHESSBGDARKMAIN)
    guiHelper.LabelPackPlacement(patronsFrame, "Patrons", guiHelper.LICHESSBGLIGHT, guiHelper.FGGRAY, guiHelper.FONT15, TOP, width=300,
                                 height=3)

    ImageFile.LOAD_TRUNCATED_IMAGES = True
    root.protocol("WM_DELETE_WINDOW", onExit)

    root.mainloop()




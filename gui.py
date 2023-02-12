import sys
import time
import tkinter.ttk
from tkinter import *

from PIL import ImageTk, Image, ImageFile

import os
import threading

from helpers import guiHelper

import common
import twitchIO as tm
import backendLogic as backend
import playerDB
import log


root = None
getPuzzlesButton = None
leftFrame, scoreboardFrame, patronsFrame, puzzleFrame, vsInfoFrame, configureFrame, puzzleInfoFrame = None, None, None, None, None, None, None
issueLabel, puzzleImageLabel, ratingLabel, themeLabel, gameUrlLabel = None, None, None, None, None
scrollCanvas = None
pb = None
sb = None

scoreboardItems = []
patronItems = []
mode = 2
moduleName = __name__

is_on = False
on = None
off = None
switchButton = None
# Define our switch function
def switch():
    global is_on

    # Determine is on or off
    if is_on:
        switchButton.config(image=off)
        getPuzzlesButton["state"] = "normal"
        is_on = False
    else:
        getPuzzlesButton["state"] = "disabled"
        onClickGetPuzzles()
        switchButton.config(image=on)
        is_on = True

def setupSwitch(container):
    global on, off, switchButton
    # Define Our Images
    onImg = Image.open("images/on.png")
    offImg = Image.open("images/off.png")


    on = ImageTk.PhotoImage (onImg.resize((40, 20)))
    off = ImageTk.PhotoImage (offImg.resize((40,20)))

    autoLabel = Label(container, text  = "AUTO SEARCH:", fg = "white", bg = guiHelper.LICHESSBGDARKMAIN)
    autoLabel.pack(side=LEFT)

    switchButton = Button(container, image=off, bd=0, command=switch, bg = guiHelper.LICHESSBGDARKMAIN, activebackground = guiHelper.LICHESSBGDARKMAIN)
    switchButton.pack(side= RIGHT)


def refreshPatrons():
    log.debugStart(moduleName, log.getFuncName())
    global patronItems



    for f in patronItems:
        f.destroy()
    y = 0
    for count, patron in enumerate(tm.subsAndStatus):
        # assign bg wrt. count
        bg = guiHelper.LICHESSBGLIGHTLIST if count % 2 == 0 else guiHelper.LICHESSBGDARKLIST
        # patron name, patron status
        name, status = patron
        # create a new ItemFrame


        frame = guiHelper.FrameOfPacksPackPlacement(scrollCanvas, (290, 40), TOP, bg)

        img = "images/patronBoss.png" if name == common.streamerName else "images/patronOnline.png" if status else "images/patronOffline.png"
        # place wing on item frame
        guiHelper.ImageOnFramePackPlacement(frame, img, (20, 20), bg, LEFT)
        # place name on item frame
        guiHelper.LabelPackPlacement(frame, name, bg, guiHelper.FGWHITE, guiHelper.LUCIDA13, LEFT)
        scrollCanvas.create_window((0, y), window=frame, anchor="nw")
        y += 40
        patronItems.append(frame)


    sb.config(command = scrollCanvas.yview)
    sb.pack( fill = Y, side = RIGHT)

    scrollCanvas.configure(yscrollcommand=sb.set)

    scrollCanvas.pack(side = LEFT)


    log.debugEnd(moduleName, log.getFuncName())


def createNewScoreboardItem(key_value, even):
    log.debugStart(moduleName, log.getFuncName())
    bg = guiHelper.LICHESSBGLIGHTLIST if even else guiHelper.LICHESSBGDARKLIST

    playerName = str(key_value[0])
    isSub = key_value[1][1]
    rtg = str(int(key_value[1][2].mu))

    newFrame = guiHelper.FrameOfPacksPackPlacement(scoreboardFrame, (300, 40), TOP, bg)

    # if user sub
    if isSub:
        img = "images/patronBoss.png" if playerName == common.streamerName else "images/patronOnline.png" if tm.isSubOnline(playerName) else "images/patronOffline.png"
    else:
        img = "images/online.png"

    guiHelper.ImageOnFramePackPlacement(newFrame, img, (20, 20), bg, LEFT)
    guiHelper.LabelPackPlacement(newFrame, playerName, bg, guiHelper.FGWHITE, guiHelper.LUCIDA13, LEFT)
    guiHelper.LabelPackPlacement(newFrame, rtg, bg, guiHelper.FGWHITE, guiHelper.LUCIDA13, RIGHT)

    log.debugEnd(moduleName, log.getFuncName())

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

        if is_on:
            time.sleep(1)
            puzzleImageLabel.destroy()
            img = Image.open("images/3.png")

            background = Image.open(imgFile)

            background.paste(img, (0, 0), img)
            background.save('NewImg.png', "PNG")

            NewImg = Image.open('NewImg.png')

            # Use Image
            test = ImageTk.PhotoImage(NewImg.resize((500, 500)))

            puzzleImageLabel = Label(puzzleFrame, width=600, height=600, image=test, bg="#262421")
            puzzleImageLabel.image = test
            puzzleImageLabel.pack()

            time.sleep(1)
            puzzleImageLabel.destroy()
            img = Image.open("images/2.png")

            background = Image.open(imgFile)

            background.paste(img, (0, 0), img)
            background.save('NewImg.png', "PNG")

            NewImg = Image.open('NewImg.png')

            # Use Image
            test = ImageTk.PhotoImage(NewImg.resize((500, 500)))

            puzzleImageLabel = Label(puzzleFrame, width=600, height=600, image=test, bg="#262421")
            puzzleImageLabel.image = test
            puzzleImageLabel.pack()

            time.sleep(1)
            puzzleImageLabel.destroy()
            img = Image.open("images/1.png")

            background = Image.open(imgFile)

            background.paste(img, (0, 0), img)
            background.save('NewImg.png', "PNG")

            NewImg = Image.open('NewImg.png')

            # Use Image
            test = ImageTk.PhotoImage(NewImg.resize((500, 500)))

            puzzleImageLabel = Label(puzzleFrame, width=600, height=600, image=test, bg="#262421")
            puzzleImageLabel.image = test
            puzzleImageLabel.pack()
            time.sleep(1)
            onClickGetPuzzles()


def showPuzzleInfo(data):
    global ratingLabel, popularityLabel, themeLabel, gameUrlLabel

    backend.puzzleRating = data[0]
    ratingLabel = Label(puzzleInfoFrame, text=f"\n{backend.puzzleRating}", bg="#262421", font=("Roboto", 15), fg="#BABAAB")
    ratingLabel.place(relx=.5, rely = .25, anchor="center")


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
    # s.theme_use('clam')
    s.configure("red.Horizontal.TProgressbar", foreground="#B47A1D", background="white")

    pb = tkinter.ttk.Progressbar(configureFrame, style="red.Horizontal.TProgressbar", mode='indeterminate', length=200)
    pb.start()
    pb.pack(side=BOTTOM)


def deleteProgressbar():
    pb.destroy()


def startReading():
    deletePuzzleInfo()
    if not is_on:
        getPuzzlesButton["state"] = "disabled"
    showProgressbar()


def stopReading():
    if not is_on:
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
    log.debugStart(moduleName, log.getFuncName())
    # save database before exit.
    playerDB.save()
    for fname in os.listdir(os.getcwd()):
        if fname.startswith("pos") or fname.startswith("outputpos"):
            os.remove(fname)
    root.destroy()
    log.debugEnd(moduleName, log.getFuncName())

def login():
    loginRoot = None
    loginErrorLabel = None
    def destroyLoginWindow():
        if common.readyDestroyLoginWindow and loginRoot is not None:
            loginRoot.destroy()
        else:
            loginRoot.after(1000, destroyLoginWindow)

    def auth_error_f():
        nonlocal loginErrorLabel
        loginErrorLabel = Label(loginRoot, text="Wrong 'username' or 'token'", fg="#B5B0B0", bg=guiHelper.LICHESSBGLIGHTLIST,
                           font=guiHelper.FONT12BOLD)
        loginErrorLabel.place(relx=0.5, rely=0.65, anchor=CENTER)

    def validateLogin():
        print(loginErrorLabel)
        if loginErrorLabel != None:
            loginErrorLabel.destroy()
        print("username entered: ", username.get())
        print("token entered :", token.get())

        tm.startTwitchIOThread(username.get(), token.get(), auth_error_f)

    def onLoginClose():
        sys.exit()

    loginRoot = guiHelper.RootWindowOfGrids("Authentication", "420x400", guiHelper.LICHESSBGLIGHTLIST)

    # get screen width and height
    screen_width = loginRoot.winfo_screenwidth()
    screen_height = loginRoot.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width / 2) - (420 / 2)
    y = (screen_height / 2) - (400 / 2)
    loginRoot.geometry('%dx%d+%d+%d' % (420, 400, x, y))

    titleLabel = Label(loginRoot, text="Login", fg = "#B5B0B0" , bg = guiHelper.LICHESSBGLIGHTLIST, font = guiHelper.FONT20).place(relx = 0.22 ,rely = 0.1, anchor = CENTER)

    usernameLabel = Label(loginRoot, text="User Name", fg = "#B5B0B0" , bg = guiHelper.LICHESSBGLIGHTLIST, font = guiHelper.FONT12BOLD).place(relx = 0.25 ,rely = 0.23, anchor = CENTER)
    username = StringVar()
    usernameEntry = tkinter.Entry(loginRoot, textvariable=username, justify = "left", bg= "#2A2E1F", fg = "#B5BAAB", font = guiHelper.FONT12, insertbackground = "#B5B0B0").place(relx = 0.5, rely = 0.3, anchor = CENTER, width = 300, height = 35)

    tokenLabel = Label(loginRoot, text="Token", fg = "#B5B0B0" , bg = guiHelper.LICHESSBGLIGHTLIST, font = guiHelper.FONT12BOLD).place(relx = 0.2 ,rely = 0.43, anchor = CENTER)
    token = StringVar()
    tokenEntry = tkinter.Entry(loginRoot, textvariable=token, show='*', justify = "left", bg= "#2A2E1F", fg = "#B5BAAB", font = guiHelper.FONT12, insertbackground = "#B5B0B0").place(relx = 0.5, rely = 0.5, anchor = CENTER, width = 300, height = 35)

    # login button
    loginButton = Button(loginRoot, text="Login", command=validateLogin, bg = "#3692E7", fg = "white", font = guiHelper.FONT12).place(relx = 0.5, rely = 0.8, anchor = CENTER, width = 300, height = 35)

    loginRoot.after(0, destroyLoginWindow)
    loginRoot.protocol("WM_DELETE_WINDOW", onLoginClose)
    loginRoot.mainloop()


def startGui():
    log.debugStart(moduleName, log.getFuncName())
    global root, nextBtn, revealBtn, puzzleFrame, \
        vsInfoFrame, issueLabel, leftFrame, \
        generateButton, configureFrame, scoreboardFrame, puzzleInfoFrame, getPuzzlesButton, patronsFrame, scrollCanvas, sb

    #################################################################################################################################################

    root = guiHelper.RootWindowOfGrids("Lichess-Twitch Streamer Puzzle Kit", "1550x750", guiHelper.LICHESSBGDARKMAIN)

    #################################################################################################################################################
    def displayAboutWindow():
        pass
    menubar = Menu(root)
    aboutMenu = Menu(menubar, tearoff = 0, background = guiHelper.LICHESSGOLD)
    aboutMenu.add_command(label = "About", command = displayAboutWindow)
    aboutMenu.add_separator()
    aboutMenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label = "Menu", menu = aboutMenu)


    root.config(menu = menubar)
    ##################################################################################################################################################

    mainFrame = guiHelper.FrameOfGridsGridPlacement(root, (600, 700), (0, 1), guiHelper.LICHESSBGLIGHTLIST)
    guiHelper.DummyFrameGridPlacement(mainFrame, (600, 25), (0, 0), guiHelper.LICHESSBGLIGHTLIST)
    puzzleFrame = guiHelper.FrameOfPacksGridPlacement(mainFrame, (600, 575), (1, 0), guiHelper.LICHESSBGLIGHTLIST)
    vsInfoFrame = guiHelper.FrameOfGridsGridPlacement(mainFrame, (600, 100), (2, 0), guiHelper.LICHESSBGLIGHTLIST)

    ###################################################################################################################################################

    leftFrame = guiHelper.FrameOfGridsGridPlacement(root, (200, 700), (0, 0), guiHelper.LICHESSBGDARKMAIN, 30, 10)

    guiHelper.DummyFrameGridPlacement(leftFrame, (200, 50), (0, 0), guiHelper.LICHESSBGDARKMAIN)

    lichesslogoFrame = guiHelper.FrameOfPacksGridPlacement(leftFrame, (200, 100), (1, 0), guiHelper.LICHESSBGDARKMAIN)
    guiHelper.ImageOnFramePackPlacement(lichesslogoFrame, "images/Lichess_logo_2019.png", (100, 100), guiHelper.LICHESSBGDARKMAIN)
    lichessOrgTitleFrame = guiHelper.FrameOfPacksGridPlacement(leftFrame, (200, 50), (2, 0), guiHelper.LICHESSBGDARKMAIN)
    guiHelper.LabelPackPlacement(lichessOrgTitleFrame, "lichess.org", guiHelper.LICHESSBGDARKMAIN, guiHelper.FGGRAY, guiHelper.FONT15, TOP, pady= 10)

    twitchLogoFrame = guiHelper.FrameOfPacksGridPlacement(leftFrame, (200, 120), (3, 0), guiHelper.LICHESSBGDARKMAIN)
    guiHelper.ImageOnFramePackPlacement(twitchLogoFrame, "images/twitch_logo_icon_189242.png", (120, 120),
                                        guiHelper.LICHESSBGDARKMAIN, TOP)
    twitchTitleFrame = guiHelper.FrameOfPacksGridPlacement(leftFrame, (200, 50), (4, 0), guiHelper.LICHESSBGDARKMAIN)
    guiHelper.LabelPackPlacement(twitchTitleFrame, "twitch.tv", guiHelper.LICHESSBGDARKMAIN, guiHelper.FGGRAY,
                                 guiHelper.FONT15, TOP)



    puzzleInfoFrame = guiHelper.FrameOfPacksGridPlacement(leftFrame, (200, 50), (5, 0), guiHelper.LICHESSBGLIGHTLIST, pady = 20)

    def flt():
        global mode
        mode = var.get()

    var = IntVar(None, 2)

    s = tkinter.ttk.Style()  # Creating style element
    s.configure('Wild.TRadiobutton',  # First argument is the name of style. Needs to end with: .TRadiobutton
                background=guiHelper.LICHESSBGLIGHTLIST,  # Setting background to our specified color above
                foreground=guiHelper.LICHESSGOLD,
                )  # You can define colors like this also

    s.configure('Dark.TRadiobutton',  # First argument is the name of style. Needs to end with: .TRadiobutton
                 background=guiHelper.LICHESSBGDARKLIST,  # Setting background to our specified color above
                 foreground=guiHelper.LICHESSGOLD,
                )  # You can define colors like this also

    R1 = tkinter.ttk.Radiobutton(leftFrame, text="Easy", variable=var, value=1, command=flt, style='Dark.TRadiobutton',
                                 width=30, takefocus = False)
    R1.grid(row=6, column=0)
    R2 = tkinter.ttk.Radiobutton(leftFrame, text="Medium", variable=var, value=2, command=flt,
                                 style='Wild.TRadiobutton', width=30, takefocus = False)
    R2.grid(row=7, column=0)
    R3 = tkinter.ttk.Radiobutton(leftFrame, text="Hard", variable=var, value=3, command=flt, style='Dark.TRadiobutton',
                                 width=30, takefocus = False)
    R3.grid(row=8, column=0)
    autoSwitchFrame = guiHelper.FrameOfPacksGridPlacement(leftFrame, width_height=(200, 40), row_col=(9, 0), bg=guiHelper.LICHESSBGDARKMAIN)
    setupSwitch(autoSwitchFrame)
    # guiHelper.DummyFrameGridPlacement(leftFrame, (200, 20), (10, 0), guiHelper.LICHESSBGDARKMAIN)

    configureFrame = guiHelper.FrameOfPacksGridPlacement(leftFrame, (200, 150), (11, 0), guiHelper.LICHESSBGLIGHTLIST)
    getPuzzlesButton = Button(configureFrame, text="SEARCH", command=onClickGetPuzzles,
                              width=30, height=3, bg="#373531", fg="#999999", borderwidth=0, highlightthickness=0,
                              activebackground="#de5100", disabledforeground="black")
    getPuzzlesButton.bind("<Enter>", lambda event: on_enter(getPuzzlesButton))
    getPuzzlesButton.bind("<Leave>", lambda event: on_leave(getPuzzlesButton))
    getPuzzlesButton.pack(side=TOP)

    issueLabel = guiHelper.LabelPackPlacement(configureFrame, "", guiHelper.LICHESSBGLIGHTLIST, guiHelper.FGWHITE, guiHelper.FONT10, BOTTOM,
                                              width=200, height=2)

    ######################################################################################################################################################

    scoreboardFrame = guiHelper.FrameOfPacksGridPlacement(root, (300, 700), (0, 2), guiHelper.LICHESSBGDARKMAIN, 30)
    guiHelper.LabelPackPlacement(scoreboardFrame, 'Puzzle Top 10', guiHelper.LICHESSBGLIGHTLIST, guiHelper.FGGRAY, guiHelper.FONT15, TOP,
                                 width=300, height=3)

    ######################################################################################################################################################
    patronsFrame = guiHelper.FrameOfPacksGridPlacement(root, (300, 700), (0, 3), guiHelper.LICHESSBGDARKMAIN)
    guiHelper.LabelPackPlacement(patronsFrame, "Patrons", guiHelper.LICHESSBGLIGHTLIST, guiHelper.FGGRAY, guiHelper.FONT15, TOP, width=300,
                                 height=3)

    scrollCanvas = Canvas(patronsFrame, width = 300, height = 700, scrollregion=(0,0,3000,3000), bg = guiHelper.LICHESSBGLIGHTLIST)
    scrollCanvas.pack_propagate(False)


    s.configure("Vertical.TScrollbar", background= guiHelper.LICHESSGOLD, bordercolor="red", arrowcolor="white")

    sb = tkinter.ttk.Scrollbar(patronsFrame, orient = "vertical")



    ImageFile.LOAD_TRUNCATED_IMAGES = True
    root.protocol("WM_DELETE_WINDOW", onExit)

    refreshPatrons()
    log.debugEnd(moduleName, log.getFuncName())

    root.mainloop()




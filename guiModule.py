import tkinter.ttk
from tkinter import *

from PIL import ImageTk, Image, ImageFile
import asyncio

import os
import threading

from twitchio.ext import commands, eventsub
import readpuzzledatabaseModule as rpdm

from glicko import WIN, LOSS
from glicko2 import Glicko2

import myGUI

puzzleRating = None
ans = None
subsAndStatus = []
scoreboard = dict()
bot = None

env = Glicko2(tau=0.5)
userRatingStart = env.create_rating(1500, 200, 0.06)

class Bot(commands.Bot):

    def __init__(self):
        print(threading.currentThread())
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token='gy0pwp2pf642rhmfulgjnekx3zzh9x', prefix=".", initial_channels=['nimoniktr'])

    async def event_ready(self):
        global subsAndStatus

        nimoniktr = await self.fetch_users(ids=[self.user_id])
        subs = await nimoniktr[0].fetch_subscriptions(token='gy0pwp2pf642rhmfulgjnekx3zzh9x')

        for sub in subs:
            subsAndStatus.append([sub.user.name, False])
        subsAndStatus.append(["yarabbi", False])

        fillAndDisplayPatronsFrame()

        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_join(self, channel, user):
        print(user.name, "joined..")
        if changeStatusOnline(user):
            sortAndDisplayScoreboard(scoreboard)
            fillAndDisplayPatronsFrame()

    async def event_part(self, user):
        print(user.name, "departed..")
        if changeStatusOffline(user):
            sortAndDisplayScoreboard(scoreboard)
            fillAndDisplayPatronsFrame()

    @commands.command(name=".")
    async def cevap(self, ctx: commands.Context):
        global ans

        ansByPlayer = ctx.message.content[3:]

        if ans == None:
            await ctx.send('Bulmaca hazır değil!.')

        elif ans == "":
            await ctx.send(f'Doğru cevap zaten verildi. Bilgisayar oynayacak. Lütfen bekle !')

        elif ans != "" and ans != None and ansByPlayer == ans:
            ans = ""
            await ctx.send(f'{ctx.author.name} doğru cevabı verdi.')
            updateScoreboard(scoreboard, WIN, ctx)
            sortAndDisplayScoreboard(scoreboard)
            rpdm.onCorrectMoveFound(showPuzzleFromDatabase)

        elif ans != "" and ans != None and ansByPlayer != ans:
            await ctx.send(f'Yanlış cevap.')

            updateScoreboard(scoreboard, LOSS, ctx)
            sortAndDisplayScoreboard(scoreboard)


def startTwitchBot():
    global bot
    bot = Bot()
    bot.run()


################################################################################


root = None
leftFrame = None
scoreboardFrame = None
patronsFrame = None

puzzleFrame = None
vsInfoFrame = None

configureFrame = None
puzzleInfoFrame = None

getPuzzlesButton = None

issueLabel = None
puzzleImageLabel = None
ratingLabel = None
themeLabel = None
gameurlLabel = None

pb = None

allPlayers = []
patronsAllFrames = []


def replace(file, pattern, subst):
    # Read contents from file as a single string
    file_handle = open(file, 'r')
    file_string = file_handle.read()
    file_handle.close()

    print("Before:", file_string)
    # Use RE package to allow for replacement (also allowing for (multiline) REGEX)
    file_string = (re.sub(pattern, subst, file_string))
    print("After:", file_string)

    # Write contents to file.
    # Using mode 'w' truncates the file.
    file_handle = open(file, 'w')
    file_handle.write(file_string)
    file_handle.close()


def getPlayerRatingFromRatingsDatabaseFile(playerName):
    with open("ratingDatabase.txt", "r") as file1:
        lines = file1.read()
        regex = fr"{playerName}\t.*$"
        matches = re.finditer(regex, lines, re.MULTILINE)

        for matchNum, match in enumerate(matches, start=1):
            playerRecord = match.group()
    tokens = playerRecord.split("\t")
    mu = tokens[1]
    sigma = tokens[2]
    volatility = tokens[3]

    return env.create_rating(float(mu), float(sigma), float(volatility))


def getPlayersFromRatingsDatabaseFile():
    dbPlayers = []
    with open("ratingDatabase.txt", "r") as file1:
        lines = file1.read()

        regex = r"^\w+\t"
        matches = re.finditer(regex, lines, re.MULTILINE)

        for matchNum, match in enumerate(matches, start=1):
            player = match.group()
            dbPlayers.append(player.strip())

    print("Databasedeki oyuncular:", dbPlayers)
    return dbPlayers

def saveRatingsToDatabaseFile():
    dbPlayers = getPlayersFromRatingsDatabaseFile()
    for key, value in scoreboard.items():
        if key in dbPlayers:
            replace("ratingDatabase.txt", r"{}.*".format(key), f"{key}\t{value[2].mu}\t{value[2].sigma}\t{value[2].volatility}")
        else:
            print("key databasede mevcut değil o yüzden a+ çalıştırıldı.")
            with open("ratingDatabase.txt", "a+") as file1:
                file1.write(f"\n{key}\t{value[2].mu}\t{value[2].sigma}\t{value[2].volatility}")


def changeStatusOnline(user):
    for e in subsAndStatus:
        if e[0] == user.name and e[1] == False:
            e[1] = True
            print("Patron status is updated: ", user.name, " is online")
            return True
    return False


def changeStatusOffline(user):
    for e in subsAndStatus:
        if e[0] == user.name and e[1] == True:
            e[1] = False
            print("Patron status is updated: ", user.name, " is offline")
            return True
    return False


def fillAndDisplayPatronsFrame():
    global patronsAllFrames

    for f in patronsAllFrames:
        f.destroy()

    for count, patron in enumerate(subsAndStatus):
        if count % 2 == 0:
            frame = myGUI.FrameOfPacksPackPlacement(patronsFrame, (300, 40), TOP, myGUI.LICHESSBGLIGHT)
            if patron[0] == "nimoniktr":
                myGUI.ImageOnFramePackPlacement(frame, "images/patronBoss.png", (20, 20), myGUI.LICHESSBGLIGHT, LEFT)
            else:
                if patron[1]:
                    myGUI.ImageOnFramePackPlacement(frame, "images/patronOnline.png", (20, 20), myGUI.LICHESSBGLIGHT,
                                                    LEFT)
                else:
                    myGUI.ImageOnFramePackPlacement(frame, "images/patron.png", (20, 20), myGUI.LICHESSBGLIGHT, LEFT)

            myGUI.LabelPackPlacement(frame, patron[0], myGUI.LICHESSBGLIGHT, myGUI.FGWHITE, ('Lucida Console', 13),
                                     LEFT)
        else:
            frame = myGUI.FrameOfPacksPackPlacement(patronsFrame, (300, 40), TOP, myGUI.LICHESSBGDARK)
            if patron[0] == "nimoniktr":
                myGUI.ImageOnFramePackPlacement(frame, "images/patronBoss.png", (20, 20), myGUI.LICHESSBGDARK, LEFT)
            else:
                if patron[1]:
                    myGUI.ImageOnFramePackPlacement(frame, "images/patronOnline.png", (20, 20), myGUI.LICHESSBGDARK,
                                                    LEFT)
                else:
                    myGUI.ImageOnFramePackPlacement(frame, "images/patron.png", (20, 20), myGUI.LICHESSBGDARK, LEFT)

            myGUI.LabelPackPlacement(frame, patron[0], myGUI.LICHESSBGDARK, myGUI.FGWHITE, ('Lucida Console', 13), LEFT)
        patronsAllFrames.append(frame)


def addNewPlayerToScoreboardFrame(value, bg, nameTxt, ratingTxt):
    newFrame = myGUI.FrameOfPacksPackPlacement(scoreboardFrame, (300, 40), TOP, bg)

    # if user sub
    if value[1] and nameTxt != "nimoniktr":
        isSubOnline = False
        for e in subsAndStatus:
            if nameTxt == e[0]:
                isSubOnline = e[1]

        if isSubOnline:
            myGUI.ImageOnFramePackPlacement(newFrame, "images/patronOnline.png", (20, 20), bg, LEFT)

            myGUI.LabelPackPlacement(newFrame, nameTxt, bg, myGUI.FGWHITE, ('Lucida Console', 13), LEFT)

            myGUI.LabelPackPlacement(newFrame, ratingTxt, bg, myGUI.FGWHITE, ('Lucida Console', 13), RIGHT)
        else:
            myGUI.ImageOnFramePackPlacement(newFrame, "images/patron.png", (20, 20), bg, LEFT)

            myGUI.LabelPackPlacement(newFrame, nameTxt, bg, myGUI.FGWHITE, ('Lucida Console', 13), LEFT)

            myGUI.LabelPackPlacement(newFrame, ratingTxt, bg, myGUI.FGWHITE, ('Lucida Console', 13), RIGHT)
    elif nameTxt == "nimoniktr":
        myGUI.ImageOnFramePackPlacement(newFrame, "images/patronBoss.png", (20, 20), bg, LEFT)

        myGUI.LabelPackPlacement(newFrame, nameTxt, bg, myGUI.FGWHITE, ('Lucida Console', 13), LEFT)

        myGUI.LabelPackPlacement(newFrame, ratingTxt, bg, myGUI.FGWHITE, ('Lucida Console', 13), RIGHT)
    else:
        myGUI.ImageOnFramePackPlacement(newFrame, "images/online.png", (20, 20), bg, LEFT)

        myGUI.LabelPackPlacement(newFrame, nameTxt, bg, myGUI.FGWHITE, ('Lucida Console', 13), LEFT)

        myGUI.LabelPackPlacement(newFrame, ratingTxt, bg, myGUI.FGWHITE, ('Lucida Console', 13), RIGHT)

    return newFrame


def updateScoreboard(scoreboard, result, ctx):
    dbPlayers = getPlayersFromRatingsDatabaseFile()
    if ctx.author.name in dbPlayers:
        userInfo = scoreboard.get(f'{ctx.author.name}', [0, ctx.author.is_subscriber, getPlayerRatingFromRatingsDatabaseFile(ctx.author.name)])
    else:
        userInfo = scoreboard.get(f'{ctx.author.name}', [0, ctx.author.is_subscriber, userRatingStart])

    playerRating = userInfo[2]

    newRating = env.rate(playerRating, [(result, env.create_rating(float(puzzleRating), 30))])
    if ctx.author.name == "yarabbi":
        userInfo[1] = True
    scoreboard[f'{ctx.author.name}'] = [userInfo[0] + 1, userInfo[1], newRating]


def sortAndDisplayScoreboard(scoreboard):
    for e in allPlayers:
        e.destroy()
    scoreboardSorted = dict(sorted(scoreboard.items(), key=lambda x: int(x[1][2].mu), reverse=True))

    for count, (key, value) in enumerate(scoreboardSorted.items()):

        nameTxt = str(key)
        ratingTxt = str(int(value[2].mu))
        if key == "reverse":
            break
        if count % 2 == 0:
            newPlayerFrame = addNewPlayerToScoreboardFrame(value, "#262421", nameTxt, ratingTxt)
        else:
            newPlayerFrame = addNewPlayerToScoreboardFrame(value, "#302E2C", nameTxt, ratingTxt)

        allPlayers.append(newPlayerFrame)


def on_enter(btn):
    if btn != None and btn['state'] == "normal":
        btn['fg'] = "white"


def on_leave(btn):
    if btn != None and btn['state'] == "normal":
        btn['fg'] = "#999999"


def placePuzzleImage(imgFile, isLastMove = False):
    global puzzleImageLabel
    if puzzleImageLabel != None:
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



def showPuzzleFromDatabase(pngFilePath, answ, isLastMove = False):
    global ans

    ans = answ

    print("answer:", ans)

    placePuzzleImage(pngFilePath, isLastMove)


def showPuzzleInfo(data):
    global ratingLabel, popularityLabel, themeLabel, gameurlLabel, puzzleRating

    puzzleRating = data[0]
    ratingLabel = Label(puzzleInfoFrame, text=f"\n{puzzleRating}", bg="#262421", font=("Roboto", 18), fg="#BABAAB")
    ratingLabel.pack()
    #
    # themeLabel = Label(vsInfoFrame, text=f"{data[2]}", bg="#262421", font=("Arial", 13), fg="#BABAAB")
    # themeLabel.pack()
    # gameurlLabel = Label(vsInfoFrame, text=f"{data[3]}", bg="#262421", font=("Arial", 13), fg="#BABAAB")
    # gameurlLabel.pack()


def deletePuzzleInfo():
    if ratingLabel != None:
        ratingLabel.destroy()
    if themeLabel != None:
        themeLabel.destroy()
    if gameurlLabel != None:
        gameurlLabel.destroy()
    issueLabel.config(text="")


def showProgressbar():
    global pb
    s = tkinter.ttk.Style()
    s.theme_use('clam')
    s.configure("red.Horizontal.TProgressbar", foreground="#B47A1D", background="white")
    # style = "red.Horizontal.TProgressbar"
    print(configureFrame)

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
    global ans
    ans = None
    issueLabel.config(text="Corrupted database try again!")
    getPuzzlesButton["state"] = "normal"


def onClickGetPuzzles():
    global ans
    ans = None
    t = threading.Thread(
        target=lambda: rpdm.getPuzzles(startReading, stopReading, showPuzzleFromDatabase, showPuzzleInfo,
                                       onExceptionOccured))
    t.start()


def onExit():
    saveRatingsToDatabaseFile()
    for fname in os.listdir(os.getcwd()):
        if fname.startswith("pos") or fname.startswith("outputpos"):
            os.remove(fname)
    root.destroy()


def startGui():
    global root, nextBtn, revealBtn, puzzleFrame, \
        vsInfoFrame, issueLabel, leftFrame, \
        generateButton, configureFrame, scoreboardFrame, puzzleInfoFrame, getPuzzlesButton, patronsFrame

    #################################################################################################################################################

    root = myGUI.RootWindowOfGrids("Lichess-Twitch Puzzle", "1550x800", myGUI.LICHESSBGDARKMAIN)

    ##################################################################################################################################################

    mainFrame = myGUI.FrameOfGridsGridPlacement(root, (600, 700), (0, 1), myGUI.LICHESSBGLIGHT)
    myGUI.DummyFrameGridPlacement(mainFrame, (600, 25), (0, 0), myGUI.LICHESSBGLIGHT)
    puzzleFrame = myGUI.FrameOfPacksGridPlacement(mainFrame, (600, 575), (1, 0), myGUI.LICHESSBGLIGHT)
    vsInfoFrame = myGUI.FrameOfGridsGridPlacement(mainFrame, (600, 100), (2, 0), myGUI.LICHESSBGLIGHT)

    ###################################################################################################################################################

    leftFrame = myGUI.FrameOfGridsGridPlacement(root, (200, 700), (0, 0), myGUI.LICHESSBGDARKMAIN, 30, 10)

    myGUI.DummyFrameGridPlacement(leftFrame, (200, 50), (0, 0), myGUI.LICHESSBGDARKMAIN)

    logoFrame = myGUI.FrameOfPacksGridPlacement(leftFrame, (200, 100), (1, 0), myGUI.LICHESSBGDARKMAIN)
    myGUI.ImageOnFramePackPlacement(logoFrame, "images/Lichess_logo_2019.png", (100, 100), myGUI.LICHESSBGDARKMAIN)

    lichessOrgFrame = myGUI.FrameOfPacksGridPlacement(leftFrame, (200, 100), (2, 0), myGUI.LICHESSBGDARKMAIN)
    myGUI.LabelPackPlacement(lichessOrgFrame, "lichess.org", myGUI.LICHESSBGDARKMAIN, myGUI.FGGRAY, myGUI.FONT15, TOP,
                             pady=10)

    streamerWingFrame = myGUI.FrameOfPacksGridPlacement(leftFrame, (200, 100), (3, 0), myGUI.LICHESSBGDARKMAIN, padY=50)
    myGUI.ImageOnFramePackPlacement(streamerWingFrame, "images/WingFlame.png", (50, 50), myGUI.LICHESSBGDARKMAIN, TOP)
    myGUI.LabelPackPlacement(streamerWingFrame, "Nimoniktr", myGUI.LICHESSBGDARKMAIN, myGUI.FGWHITE, myGUI.FONT15,
                             BOTTOM)

    puzzleInfoFrame = myGUI.FrameOfPacksGridPlacement(leftFrame, (200, 80), (4, 0), myGUI.LICHESSBGLIGHT)

    myGUI.DummyFrameGridPlacement(leftFrame, (200, 50), (5, 0), myGUI.LICHESSBGDARKMAIN)

    configureFrame = myGUI.FrameOfPacksGridPlacement(leftFrame, (200, 100), (6, 0), myGUI.LICHESSBGLIGHT)
    getPuzzlesButton = Button(configureFrame, text="Random Puzzle", command=onClickGetPuzzles,
                              width=30, height=3, bg="#373531", fg="#999999", borderwidth=0, highlightthickness=0,
                              activebackground="#de5100", disabledforeground="black")
    getPuzzlesButton.bind("<Enter>", lambda event: on_enter(getPuzzlesButton))
    getPuzzlesButton.bind("<Leave>", lambda event: on_leave(getPuzzlesButton))
    getPuzzlesButton.pack(side=TOP)

    issueLabel = myGUI.LabelPackPlacement(configureFrame, "", myGUI.LICHESSBGLIGHT, myGUI.FGWHITE, myGUI.FONT10, BOTTOM,
                                          width=200, height=2)

    ######################################################################################################################################################

    scoreboardFrame = myGUI.FrameOfPacksGridPlacement(root, (300, 700), (0, 2), myGUI.LICHESSBGDARKMAIN, 30)
    myGUI.LabelPackPlacement(scoreboardFrame, 'Puzzle Top 10', myGUI.LICHESSBGLIGHT, myGUI.FGGRAY, myGUI.FONT15, TOP,
                             width=300, height=3)

    ######################################################################################################################################################
    patronsFrame = myGUI.FrameOfPacksGridPlacement(root, (300, 700), (0, 3), myGUI.LICHESSBGDARKMAIN)
    myGUI.LabelPackPlacement(patronsFrame, "Patrons", myGUI.LICHESSBGLIGHT, myGUI.FGGRAY, myGUI.FONT15, TOP, width=300,
                             height=3)

    ImageFile.LOAD_TRUNCATED_IMAGES = True
    root.protocol("WM_DELETE_WINDOW", onExit)

    root.mainloop()


#######################################################################################################################################################
#######################################################################################################################################################
#######################################################################################################################################################


event_loop_a = asyncio.new_event_loop()


def run_loop(loop):
    asyncio.set_event_loop(loop)
    startTwitchBot()
    loop.run_forever()


twitchthread = threading.Thread(target=lambda: run_loop(event_loop_a), daemon=True)
twitchthread.start()

threading.Thread(target=startGui).start()

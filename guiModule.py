import tkinter.ttk
from tkinter import *

from PIL import ImageTk, Image, ImageFile
import asyncio

import os
import threading

from twitchio.ext import commands, pubsub
from twitchio import PartialUser
import readpuzzledatabaseModule as rpdm

from glicko import Glicko, WIN, DRAW, LOSS
from glicko2 import Glicko2

rating = None
ans = None
subs = None
scoreboard = dict()
bot = None

env = Glicko2(tau= 0.5)
userRatingStart = env.create_rating(1500, 200, 0.06)

class Bot(commands.Bot):

    def __init__(self):
        print(threading.currentThread())
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token='gy0pwp2pf642rhmfulgjnekx3zzh9x', prefix=".", initial_channels=['nimoniktr'])

    async def event_ready(self):
        global subs
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        nimoniktr = await self.fetch_users(ids=[self.user_id])
        subs = await nimoniktr[0].fetch_subscriptions(token= 'gy0pwp2pf642rhmfulgjnekx3zzh9x')
        setupPatronsFrame(subs)

        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    @commands.command(name= ".")
    async def cevap(self, ctx: commands.Context):
        global ans
        ansByPlayer = ctx.message.content[3:]
        if ans == None:
            await ctx.send('Bulmaca hazır değil!.')
        elif ans == "":
            await ctx.send(f'Doğru cevap zaten verildi. Bilgisayar oynayacak. Lütfen bekle !')
        elif ans != "" and ans != None and  ansByPlayer == ans:
            await ctx.send(f'{ctx.author.name} doğru cevabı verdi.')
            ans = ""

            userInfo = scoreboard.get(f'{ctx.author.name}', (0, ctx.author.is_vip, userRatingStart))

            playerRating = userInfo[2]

            newRating = env.rate(playerRating, [(WIN, env.create_rating(int(rating), 30))])

            print("uSERINFO2: ", userInfo[2])
            scoreboard[f'{ctx.author.name}'] = (userInfo[0] + 1, userInfo[1], newRating)
            onPlayerFindsAnswer(scoreboard)
            rpdm.onCorrectMoveFound(showPuzzleFromDatabase)
        elif ans != "" and ans != None and ansByPlayer != ans:

            userInfo = scoreboard.get(f'{ctx.author.name}', (0, ctx.author.is_vip, userRatingStart))

            playerRating = userInfo[2]

            newRating = env.rate(playerRating, [(LOSS, env.create_rating(int(rating), 30))])

            print("uSERINFO2: ", userInfo[2])
            scoreboard[f'{ctx.author.name}'] = (userInfo[0] + 1, userInfo[1], newRating)
            onPlayerFindsAnswer(scoreboard)

            await ctx.send(f'Yanlış cevap.')



def startTwitchBot():
    global bot
    bot = Bot()
    bot.run()
################################################################################


root = None
leftFrame = None
rightFrame=None
patronFrame = None

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

framesInScoreboard = []

def setupPatronsFrame(patrons):
    for patron in patrons:
        frame = Frame(patronFrame, width=300, height=50, bg= "#262421")
        frame.pack_propagate(False)
        frame.pack(side=TOP)

        wingImg = Image.open("images/patron.png")
        wingImg = wingImg.resize((20, 20))
        img = ImageTk.PhotoImage(wingImg)
        canvas = Canvas(frame, width=40, height=20, bg="#262421", borderwidth=0, highlightthickness=0)
        canvas.create_image(10, 0, image=img, anchor=NW)
        canvas.image = img
        canvas.pack(side=LEFT)

        contesterLabel = Label(frame, text=patron.user.name, bg="#262421", fg="#BABAAB", font=('Lucida Console', 13))
        contesterLabel.pack(side=LEFT)


def setupScoreboardFrame(value, bg, txt):

    frame = Frame(rightFrame, width=300, height=50, bg=bg)
    frame.pack_propagate(False)
    frame.pack(side=TOP)

    if value[1]:
        print("vip:", value)
        wingImg = Image.open("images/patron.png")
        wingImg = wingImg.resize((20, 20))
        img = ImageTk.PhotoImage(wingImg)
        canvas = Canvas(frame, width=40, height=20, bg=bg, borderwidth=0, highlightthickness=0)
        canvas.create_image(10, 0, image=img, anchor=NW)
        canvas.image = img
        canvas.pack(side=LEFT)

        contesterLabel = Label(frame, text=txt, bg=bg, fg="#BABAAB", font=('Lucida Console', 13))
        contesterLabel.pack(side=RIGHT)
    else:
        contesterLabel = Label(frame, text=txt, width=200, bg="red", fg="white",
                               font=('Lucida Console', 14))
        contesterLabel.pack(side=RIGHT)

        return frame

def onPlayerFindsAnswer(scoreboard):
    for e in framesInScoreboard:
        e.destroy()
    scoreboardSorted = dict(sorted(scoreboard.items(), key= lambda x:int(x[1][2].mu), reverse = True))

    for count, (key, value) in enumerate(scoreboardSorted.items()):


        # txt = '{}{}'.format(str(key).ljust(20), str(value[0]).rjust(4))
        txt = '{}{}'.format(str(key).ljust(20), str(int(value[2].mu)).rjust(4))

        if key == "reverse":
            break
        if count % 2 == 0:
            contesterFrame = setupScoreboardFrame(value, "#262421", txt)
        else:
            contesterFrame =  setupScoreboardFrame(value, "#302E2C", txt)

        framesInScoreboard.append(contesterFrame)

def onPlayerFindsAnswerRating():
    pass
def on_enter(btn):
    if btn != None and btn['state'] == "normal":
        btn['fg'] = "white"

def on_leave(btn):
    if btn != None and btn['state'] == "normal":
        btn['fg'] = "#999999"



def placePuzzleImage(imgFile):
    global puzzleImageLabel
    if puzzleImageLabel != None:
        puzzleImageLabel.destroy()

    img = Image.open(imgFile)

    # Create a photoimage object of the image in the path
    test = ImageTk.PhotoImage(img.resize((500, 500)))

    puzzleImageLabel = Label(puzzleFrame, width = 600, height = 600, image=test, bg="#262421")
    puzzleImageLabel.image = test

    # Position image
    puzzleImageLabel.pack()

def showPuzzleFromDatabase(pngFilePath, answ):
    global ans

    ans = answ

    print("answer:", ans)

    placePuzzleImage(pngFilePath)

def showPuzzleInfo(data):
    global ratingLabel, popularityLabel, themeLabel, gameurlLabel, rating

    rating = data[0]
    ratingLabel = Label(puzzleInfoFrame, text = f"\n{rating}" , bg = "#262421", font = ("Arial", 15), fg="#BABAAB")
    ratingLabel.pack()

    themeLabel = Label(vsInfoFrame, text = f"{data[2]}", bg = "#262421", font = ("Arial", 13), fg="#BABAAB")
    themeLabel.pack()
    gameurlLabel = Label(vsInfoFrame, text = f"{data[3]}", bg = "#262421", font = ("Arial", 13), fg="#BABAAB")
    gameurlLabel.pack()

def deletePuzzleInfo():
    if ratingLabel != None:
        ratingLabel.destroy()
    if themeLabel != None:
        themeLabel.destroy()
    if gameurlLabel != None:
        gameurlLabel.destroy()
    issueLabel.config(text = "")

def showProgressbar():
    global pb
    s = tkinter.ttk.Style()
    s.theme_use('clam')
    s.configure("red.Horizontal.TProgressbar", foreground="#B47A1D", background= "white")
    # style = "red.Horizontal.TProgressbar"
    print(configureFrame)

    pb = tkinter.ttk.Progressbar(configureFrame, style = "red.Horizontal.TProgressbar",  mode='indeterminate', length=200)
    pb.start()
    pb.pack(side = BOTTOM)

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
    issueLabel.config(text= "Corrupted database try again!")
    getPuzzlesButton["state"] = "normal"

def onClickGetPuzzles():
    global ans
    ans = None
    t = threading.Thread(target=lambda : rpdm.getPuzzles(startReading, stopReading, showPuzzleFromDatabase, showPuzzleInfo, onExceptionOccured))
    t.start()

def on_closing():
    for fname in os.listdir(os.getcwd()):
        if fname.startswith("pos") or fname.startswith("outputpos"):
            os.remove(fname)
    root.destroy()

def startGui():
    global root, nextBtn, revealBtn, puzzleFrame, \
        vsInfoFrame, issueLabel, leftFrame, \
        generateButton, configureFrame, rightFrame, puzzleInfoFrame, getPuzzlesButton, patronFrame

    root = Tk()
    root.title("Lichess-Twitch Puzzle")
    root.resizable(False, False)
    root.config(bg = "#161512")

    root.geometry("1550x800")
    root.grid_propagate(False)

    mainFrame = Frame(root, width=600, height=700, bg= "#262421")
    mainFrame.grid_propagate(False)
    mainFrame.grid(row=0, column=1, padx = 10)

    dummyFrameMain = Frame(mainFrame, width = 600, height = 25, bg= "#262421")
    dummyFrameMain.grid(row= 0, column = 0)

    puzzleFrame = Frame(mainFrame, width=600, height=575, bg= "#262421")
    puzzleFrame.pack_propagate(False)
    puzzleFrame.grid(row=1, column = 0)

    vsInfoFrame = Frame(mainFrame, width = 600, height = 100, bg = "#262421")
    vsInfoFrame.grid_propagate(False)
    vsInfoFrame.grid(row = 2, column = 0)

    leftFrame = Frame(root, width=200, height=700)
    leftFrame.grid_propagate(False)
    leftFrame.config(bg = "#161512")
    leftFrame.grid(row=0, column=0, padx=30, pady=10)

    rightFrame = Frame(root, width = 300, height = 700)
    rightFrame.pack_propagate(False)
    rightFrame.config(bg = "#161512")
    rightFrame.grid(row=0, column = 2, padx = 10)

    scoreboardTitle = Label(rightFrame, text=f'Puzzle Top 10', width=300, height=3, bg="#262421", fg="#BABAAB", font = ("Arial", 15))
    scoreboardTitle.pack(side = TOP)

    patronFrame = Frame(root, width=300, height=700)
    patronFrame.pack_propagate(False)
    patronFrame.config(bg="#161512")
    patronFrame.grid(row=0, column=3)

    patronsTitle = Label(patronFrame, text=f'Patrons', width=300, height=3, bg="#262421", fg="#BABAAB",
                            font=("Arial", 15))
    patronsTitle.pack(side=TOP)

    logoFrame = Frame(leftFrame, width=200, height=100, bg = "#161512")
    logoFrame.pack_propagate(False)
    logoFrame.grid(row=1, column=0)

    dummyFrame2 = Frame(leftFrame, width=200, height=150, bg = "#161512")
    dummyFrame2.pack_propagate(False)
    dummyFrame2.grid(row=2, column=0)

    dummyFrame = Frame(leftFrame, width=200, height=50, bg="#161512")
    dummyFrame.pack_propagate(False)
    dummyFrame.grid(row=0, column=0)

    puzzleInfoFrame = Frame(leftFrame, width=200, height=100, bg="#262421")
    puzzleInfoFrame.pack_propagate(False)
    puzzleInfoFrame.grid(row=3, column=0)

    dummyFrame3 = Frame(leftFrame, width=200, height=50, bg="#161512")
    dummyFrame3.pack_propagate(False)
    dummyFrame3.grid(row=4, column=0)

    lichessOrgLabel = Label(dummyFrame2, text = "lichess.org", fg = "#BABABA", bg = "#161512", font = ("Arial", 15))
    lichessOrgLabel.pack(pady = 10)

    configureFrame = Frame(leftFrame, width=200, height= 100, bg= "#262421")
    configureFrame.pack_propagate(False)
    configureFrame.grid(row=5, column=0)


    logoImg = Image.open("images/Lichess_logo_2019.png")
    logoImg = logoImg.resize((100, 100))
    img = ImageTk.PhotoImage(logoImg)
    canvas = Canvas(logoFrame, bg="#161512", borderwidth = 0, highlightthickness = 0)
    canvas.create_image(50, 0, image = img, anchor = NW)
    canvas.pack()

    getPuzzlesButton = Button(configureFrame, text="Random Puzzle", command= onClickGetPuzzles,
                            width=30, height=3, bg="#373531", fg="#999999", borderwidth=0, highlightthickness=0,
                            activebackground="#de5100", disabledforeground="black")
    getPuzzlesButton.bind("<Enter>", lambda event: on_enter(getPuzzlesButton))
    getPuzzlesButton.bind("<Leave>", lambda event: on_leave(getPuzzlesButton))
    getPuzzlesButton.pack(side=TOP)

    issueLabel = Label(configureFrame, width =200,height = 2, bg= "#262421", fg = "#999999")
    issueLabel.pack(side = BOTTOM)

    ImageFile.LOAD_TRUNCATED_IMAGES = True

    root.protocol("WM_DELETE_WINDOW", on_closing)


    root.mainloop()


#######################################################################################################
#######################################################################################################

event_loop_a = asyncio.new_event_loop()
def run_loop(loop):
    asyncio.set_event_loop(loop)
    startTwitchBot()
    loop.run_forever()

twitchthread = threading.Thread(target = lambda: run_loop(event_loop_a), daemon=True)
twitchthread.start()


threading.Thread(target = startGui).start()


import tkinter.ttk
from tkinter import *
from PIL import ImageTk, Image, ImageFile
import asyncio

import main
import os
import threading

from twitchio.ext import commands
import readpuzzledatabaseModule as rpdm

isPuzzleReady = False
ans = None

scoreboard = dict()
bot = None
class Bot(commands.Bot):

    def __init__(self):
        print(threading.currentThread())
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token='1b2wcds4ipwp1qm3atlbpdm4t4m62j', prefix='?', initial_channels=['nimoniktr'])

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    @commands.command(name= "")
    async def cevap(self, ctx: commands.Context):
        global ans
        if not isPuzzleReady:
            await ctx.send(f'Puzzle not ready!')
        else:
            if ans != "" and ctx.message.content[7:] == ans:
                await ctx.send(f'{ctx.author.name} doğru cevabı verdi.')
                ans = ""
                scoreboard[f'{ctx.author.name}'] = scoreboard.get(f'{ctx.author.name}', 0) + 1
                onPlayerFindsAnswer(scoreboard)
                rpdm.onCorrectMoveFound(showPuzzleFromDatabase)

            elif ans == "":
                await ctx.send(f'Doğru cevap zaten verildi. Bilgisayar oynayacak. Lütfen bekle !')
            else:
                await ctx.send(f'Yanlış cevap.')

def startTwitchBot():
    global bot
    bot = Bot()

    bot.run()




################################################################################









index = 0
revealed = False

root = None
vsInfoLabel = None
answerLabel = None
blackNameLabel = None
nextButton: Button = None
revealBtn: Button = None
puzzleFrame = None
vsInfoFrame = None
issueLabel = None
puzzleLabel = None
leftFrame = None
generateButton = None
configureFrame = None
pb = None
rightFrame=None
labelsInScoreboard = []



def onPlayerFindsAnswer(scoreboard):
    for lblinScoreboard in labelsInScoreboard:
        lblinScoreboard.destroy()
    scoreboardSorted = dict(sorted(scoreboard.items(), key= lambda x:x[1], reverse = True))
    print(scoreboardSorted)
    for count, (key, value) in enumerate(scoreboardSorted.items()):
        if key == "reverse":
            break
        if count % 2 == 0:
            contesterLabel = Label(rightFrame, text = f'{count + 1}        {key}          {value}', width = 200, height = 3, bg = "#262421", fg="#BABAAB")
        else:
            contesterLabel = Label(rightFrame, text=f'{count + 1}        {key}          {value}', width=200, height=3, bg="#302E2C", fg="#BABAAB")
        labelsInScoreboard.append(contesterLabel)
        contesterLabel.pack(side=TOP)



def on_enter(btn):
    if btn != None and btn['state'] == "normal":
        btn['fg'] = "white"

def on_leave(btn):
    if btn != None and btn['state'] == "normal":
        btn['fg'] = "#999999"

def onClickNext(puzzleInfo):
    print("next clicked.")
    global index, revealed, ans
    index += 1

    if index > len(puzzleInfo) - 1:
        index = 0

    onAfter()
    issueLabel.config(text="{} out of {} showing...".format(index + 1, len(puzzleInfo)))
    placePuzzleImage(puzzleInfo[index][0])
    ans = puzzleInfo[index][1]
    if revealed:
        vsInfoLabel.destroy()
        answerLabel.destroy()

        revealed = False

def placePuzzleImage(imgFile):
    global puzzleLabel
    if puzzleLabel != None:
        puzzleLabel.destroy()

    img = Image.open(imgFile)

    # Create a photoimage object of the image in the path
    test = ImageTk.PhotoImage(img.resize((500, 500)))

    puzzleLabel = Label(puzzleFrame, width = 600, height = 600,  image=test,  bg= "#262421")
    puzzleLabel.image = test

    # Position image
    puzzleLabel.pack()

# puzzleInfo ----> [(outputFile, ans, game), ....]
def onClickReveal(puzzleInfo):
    print("reveal clicked.")
    global revealed, vsInfoLabel, answerLabel, blackNameLabel
    if revealed == False:
        gm = puzzleInfo[index][2]
        whiteName = gm.white
        whiteElo = gm.whiteElo
        blackName = gm.black
        blackElo = gm.blackElo

        vsInfoLabel = Label(vsInfoFrame, text =whiteName[8:-2] + "     " + whiteElo[11:-2] + "                         " +
                                                    blackElo[11: -2] + "     " + blackName[8:-2],
                            font = ('Noto Sans', 10), bg= "#262421", fg = "#B47A1D")
        vsInfoLabel.place(anchor = CENTER, relx = .5, rely = .3)

        answerLabel = Label(vsInfoFrame, text =  puzzleInfo[index][1], bg ="#262421", fg ="#5B8D23", font = ('Noto Sans', 15))
        answerLabel.place(anchor = CENTER, relx = .5, rely = .6)

        revealed = True
def onAfter():
    issueLabel.config(text = "")
def showPuzzles(puzzleInfo):
    global nextBtn, revealBtn, isPuzzleReady, ans
    if len(puzzleInfo) > 0:

        placePuzzleImage(puzzleInfo[0][0])
        issueLabel.config(text="{} out of {} showing...".format(index + 1, len(puzzleInfo)))

        nextBtn.config(state = "normal", command = lambda: onClickNext(puzzleInfo))
        revealBtn.config(state = "normal", command = lambda: onClickReveal(puzzleInfo))
        isPuzzleReady = True
        ans = puzzleInfo[0][1]
    else:
        issueLabel.config(text="No puzzle found!")

def showPuzzleFromDatabase(pngFilePath, answ):
    global isPuzzleReady, ans

    isPuzzleReady = True
    ans = answ

    print("answer:", ans)

    placePuzzleImage(pngFilePath)

def showWarning1():
    issueLabel.config(text= "Please fill the area.")
    issueLabel.after(1000, onAfter)
    generateButton["state"] = "normal"

def showWarning2():
    issueLabel.config(text="Wrong username!")
    generateButton["state"] = "normal"

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
    showProgressbar()

def stopReading():
    deleteProgressbar()

def endThread():
    deleteProgressbar()
    generateButton["state"] = "normal"

def onClickGetPuzzles():
    global ans
    ans = None
    t = threading.Thread(target=lambda : rpdm.getPuzzles(startReading, stopReading, showPuzzleFromDatabase))
    t.start()
def onClickGenerateStartThread(entry):
    global isPuzzleReady
    isPuzzleReady = False
    global revealed, index
    if puzzleLabel != None:
        puzzleLabel.destroy()
    if vsInfoLabel != None:
        vsInfoLabel.destroy()
    if blackNameLabel != None:
        blackNameLabel.destroy()
    if answerLabel != None:
        answerLabel.destroy()

    revealed = False
    index = 0
    for fname in os.listdir(os.getcwd()):
        if fname.startswith("pos") or fname.startswith("Outputpos"):
            os.remove(fname)

    generateButton["state"] = "disabled"
    generateButton['fg'] = "#999999"
    if nextBtn != None:
        nextBtn["state"] ="disabled"
        nextBtn['fg'] = "#999999"
    if revealBtn != None:
        revealBtn["state"] = "disabled"
        revealBtn['fg'] = "#999999"

    t = threading.Thread(target= lambda: main.main(entry, showPuzzles, showWarning1, showWarning2, showProgressbar, endThread, log))
    t.start()

def log(msg):
    issueLabel.config(text = msg)


def on_closing():

    for fname in os.listdir(os.getcwd()):
        if fname.startswith("pos") or fname.startswith("outputpos"):
            os.remove(fname)
    root.destroy()


def startGui():

    global root, nextBtn, revealBtn, puzzleFrame, vsInfoFrame, issueLabel, leftFrame, generateButton, configureFrame, rightFrame

    root = Tk()
    root.title("Lichess Puzzle Generator")
    root.resizable(False, False)
    root.config(bg = "#161512")

    root.geometry("1100x800")
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

    rightFrame = Frame(root, width = 200, height = 700)
    rightFrame.pack_propagate(False)
    rightFrame.config(bg = "#161512")
    rightFrame.grid(row=0, column = 2)

    scoreboardLabel = Label(rightFrame, text=f'Puzzle Top 10', width=200, height=3, bg="#262421", fg="#BABAAB", font = ("Arial", 15))
    scoreboardLabel.pack(side = TOP)

    logoFrame = Frame(leftFrame, width=200, height=100, bg = "#161512")
    logoFrame.pack_propagate(False)
    logoFrame.grid(row=1, column=0)

    dummyFrame2 = Frame(leftFrame, width=200, height=250, bg = "#161512")
    dummyFrame2.pack_propagate(False)
    dummyFrame2.grid(row=2, column=0)

    dummyFrame = Frame(leftFrame, width=200, height=50, bg="#161512")
    dummyFrame.pack_propagate(False)
    dummyFrame.grid(row=0, column=0)

    lichessOrgLabel = Label(dummyFrame2, text = "lichess.org", fg = "#BABABA", bg = "#161512", font = ("Arial", 15))
    lichessOrgLabel.pack(pady = 10)

    configureFrame = Frame(leftFrame, width=200, height= 100, bg= "#262421")
    configureFrame.pack_propagate(False)
    configureFrame.grid(row=3, column=0)


    logoImg = Image.open("images/Lichess_logo_2019.png")
    logoImg = logoImg.resize((100, 100))
    img = ImageTk.PhotoImage(logoImg)
    canvas = Canvas(logoFrame, bg="#161512", borderwidth = 0, highlightthickness = 0)
    canvas.create_image(50, 0, image = img, anchor = NW)
    canvas.pack()



    # nextBtn = Button(configureFrame, text="Next", width = 30, height = 3,  bg = "#373531", borderwidth = 0, highlightthickness = 0, activebackground = "#de5100", disabledforeground="black",  fg = "#999999")
    # nextBtn.bind("<Enter>", lambda event : on_enter(nextBtn))
    # nextBtn.bind("<Leave>", lambda event : on_leave(nextBtn))
    # nextBtn.config(state = "disabled")
    # nextBtn.pack(side = BOTTOM)


    # revealBtn = Button(configureFrame, text="Reveal", width= 30, height = 3,  bg = "#373531", borderwidth = 0, highlightthickness = 0, activebackground = "#de5100", disabledforeground="black",  fg = "#999999")
    # revealBtn.bind("<Enter>", lambda event : on_enter(revealBtn))
    # revealBtn.bind("<Leave>", lambda event : on_leave(revealBtn))
    # revealBtn.config(state="disabled")
    # revealBtn.pack(side = BOTTOM)


    # e = Entry(configureFrame, bd = 3, width = 40)
    # e.pack(side = TOP)


    getPuzzlesButton = Button(configureFrame, text="Random Puzzle", command= onClickGetPuzzles,
                            width=30, height=3, bg="#373531", fg="#999999", borderwidth=0, highlightthickness=0,
                            activebackground="#de5100", disabledforeground="black")
    getPuzzlesButton.bind("<Enter>", lambda event: on_enter(generateButton))
    getPuzzlesButton.bind("<Leave>", lambda event: on_leave(generateButton))
    getPuzzlesButton.pack(side=TOP)

    # generateButton = Button(configureFrame, text = "Generate!", command = lambda: onClickGenerateStartThread(e.get()), width = 30, height = 3, bg = "#373531", fg = "#999999",  borderwidth = 0, highlightthickness = 0, activebackground = "#de5100", disabledforeground="black")
    # generateButton.bind("<Enter>", lambda event : on_enter(generateButton))
    # generateButton.bind("<Leave>", lambda event : on_leave(generateButton))
    # generateButton.pack(side = TOP)


    issueLabel = Label(configureFrame, width =200,height = 2, bg= "#262421", fg = "#999999")
    issueLabel.pack(side = TOP)

    ImageFile.LOAD_TRUNCATED_IMAGES = True

    root.protocol("WM_DELETE_WINDOW", on_closing)


    root.mainloop()


event_loop_a = asyncio.new_event_loop()
def run_loop(loop):
    asyncio.set_event_loop(loop)
    startTwitchBot()
    loop.run_forever()

twitchthread = threading.Thread(target = lambda: run_loop(event_loop_a), daemon=True)
twitchthread.start()


threading.Thread(target = startGui).start()


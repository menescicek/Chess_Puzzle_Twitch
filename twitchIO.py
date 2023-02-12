import common
import backendLogic as backend
import playerDB
import asyncio
import threading
import twitchio
from twitchio.ext import commands
from helpers.glicko import WIN, LOSS
import log

twitchThread, bot = None, None
subsAndStatus = []

moduleName = __name__


class Bot(commands.Bot):
    def __init__(self, username, token, auth_error_f):
        self.username = username
        self.token = token
        self.auth_error_f = auth_error_f
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=token, prefix=".", initial_channels=[self.username])

    async def event_ready(self):
        global subsAndStatus
        log.debugStart(moduleName, log.getFuncName())

        if self.username != self.nick:
            await self.close()
            self.auth_error_f()
            return

        playerDB.dbPlayers = playerDB.getPlayers()

        nimoniktr = await self.fetch_users(ids=[self.user_id])
        subs = await nimoniktr[0].fetch_subscriptions(token=self.token)
        for sub in subs:
            subsAndStatus.append([sub.user.name, False])

        common.streamerName = self.nick
        common.readyDestroyLoginWindow = True
        common.readyOpenMainWindow = True

        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

        log.debugEnd(moduleName, log.getFuncName())

    async def event_join(self, channel, user):
        log.debugStart(moduleName, log.getFuncName())
        print(user.name, "joined..")
        if changeStatusOnline(user):
            backend.refreshScoreboardItems()
            common.refreshPatrons()
        log.debugEnd(moduleName, log.getFuncName())

    async def event_part(self, user):
        log.debugStart(moduleName, log.getFuncName())
        print(user.name, "departed..")
        if changeStatusOffline(user):
            backend.refreshScoreboardItems()
            common.refreshPatrons()
        log.debugEnd(moduleName, log.getFuncName())

    @commands.command(name=".")
    async def cevap(self, ctx: commands.Context):
        log.debugStart(moduleName, log.getFuncName())
        ansByPlayer = ctx.message.content[3:]

        if backend.puzzleAnswer is None:
            await ctx.send('Bulmaca hazır değil!.')

        elif backend.puzzleAnswer == "":
            await ctx.send(f'Doğru cevap zaten verildi. Bilgisayar oynayacak. Lütfen bekle !')

        elif backend.puzzleAnswer != "" and backend.puzzleAnswer is not None and ansByPlayer == backend.puzzleAnswer:
            await ctx.send(f'{ctx.author.name} doğru cevabı verdi.')

            backend.puzzleAnswer = ""

            backend.updateScoreboardDict(WIN, ctx)
            backend.refreshScoreboardItems()

            common.onCorrectMoveFound()
        elif backend.puzzleAnswer != "" and backend.puzzleAnswer is not None and ansByPlayer != backend.puzzleAnswer:
            await ctx.send(f'Yanlış cevap.')

            backend.updateScoreboardDict(LOSS, ctx)
            backend.refreshScoreboardItems()
        log.debugEnd(moduleName, log.getFuncName())


def changeStatusOnline(user):
    log.debugStart(moduleName, log.getFuncName(), subsAndStatus)
    for e in subsAndStatus:
        if e[0] == user.name and e[1] == False:
            e[1] = True
            print("Patron status is updated: ", user.name, " is online")
            log.debugEnd(moduleName, log.getFuncName(), subsAndStatus)
            return True
    log.debugEnd(moduleName, log.getFuncName(), subsAndStatus)
    return False


def changeStatusOffline(user):
    log.debugStart(moduleName, log.getFuncName(), subsAndStatus)
    for e in subsAndStatus:
        if e[0] == user.name and e[1] == True:
            e[1] = False
            print("Patron status is updated: ", user.name, " is offline")
            log.debugEnd(moduleName, log.getFuncName(), subsAndStatus)
            return True
    log.debugEnd(moduleName, log.getFuncName(), subsAndStatus)
    return False


def isSubOnline(thisSub):
    for e in subsAndStatus:
        sub, stat = e
        if sub == thisSub:
            return stat
    return None


def startTwitchBot(username, token, auth_error_f):
    global bot

    try:
        bot = Bot(username, token, auth_error_f)
    except Exception as e:
        print("Bot can not be created.. ", e)
    try:
        bot.run()
    except twitchio.errors.AuthenticationError as e:
        print(e)
        auth_error_f()
    except Exception as e:
        print("Error: ", e)


def startTwitchIOThread(username, token, errorFunc):
    global twitchThread
    policy = asyncio.get_event_loop_policy()
    policy._loop_factory = asyncio.SelectorEventLoop
    event_loop_a = asyncio.new_event_loop()

    def run_loop(loop):

        asyncio.set_event_loop(loop)
        startTwitchBot(username, token, errorFunc)
        try:
            loop.run_forever()
        except RuntimeError as e:
            print(e)

    twitchThread = threading.Thread(target=lambda: run_loop(event_loop_a), daemon= True)
    twitchThread.start()
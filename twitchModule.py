import common
import backendLogic as backend
from twitchio.ext import commands
from glicko import WIN, LOSS

bot = None
subsAndStatus = []


class Bot(commands.Bot):
    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token='gy0pwp2pf642rhmfulgjnekx3zzh9x', prefix=".", initial_channels=['nimoniktr'])

    async def event_ready(self):
        global subsAndStatus

        nimoniktr = await self.fetch_users(ids=[self.user_id])
        subs = await nimoniktr[0].fetch_subscriptions(token='gy0pwp2pf642rhmfulgjnekx3zzh9x')
        backend.dbPlayers = backend.getPlayersFromRatingsDatabaseFile()

        for sub in subs:
            subsAndStatus.append([sub.user.name, False])
        subsAndStatus.append(["yarabbi", False])

        common.fillAndDisplayPatronsFrame()

        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_join(self, channel, user):
        print(user.name, "joined..")
        if common.changeStatusOnline(user):
            backend.refreshScoreboardItems()
            common.fillAndDisplayPatronsFrame()

    async def event_part(self, user):
        print(user.name, "departed..")
        if common.changeStatusOffline(user):
            backend.refreshScoreboardItems()
            common.fillAndDisplayPatronsFrame()

    @commands.command(name=".")
    async def cevap(self, ctx: commands.Context):

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


def startTwitchBot():
    global bot
    bot = Bot()
    bot.run()

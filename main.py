import asyncio
import common
import threading
import twitchModule


event_loop_a = asyncio.new_event_loop()


def run_loop(loop):
    asyncio.set_event_loop(loop)
    twitchModule.startTwitchBot()
    loop.run_forever()


twitchThread = threading.Thread(target=lambda: run_loop(event_loop_a), daemon=True)
twitchThread.start()

common.startGui()

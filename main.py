import asyncio
import common
import threading
import twitchModule



event_loop_a = asyncio.new_event_loop()


def run_loop(loop):
    asyncio.set_event_loop(loop)
    twitchModule.startTwitchBot()
    loop.run_forever()


twitchthread = threading.Thread(target=lambda: run_loop(event_loop_a), daemon= True)
twitchthread.start()

common.startGui()

# threading.Thread(target=common.startGui).start()
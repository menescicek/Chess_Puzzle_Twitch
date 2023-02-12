import common

from waiting import wait

common.login()

def is_something_ready(something):
    if something:
        return True
    return False


wait(lambda: is_something_ready(common.readyOpenMainWindow), timeout_seconds=120, waiting_for="something to be ready")
# this code will only execute after "something" is ready

common.startGui()



"""import time
from threading import Timer


def display(msg):
    print(msg + ' ' + time.strftime('%H:%M:%S'))


class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


timer = RepeatTimer(1, display, ['Repeating'])
timer.start()
time.sleep(5)
timer.cancel()
"""
import time
from contextlib import contextmanager
from threading import Thread

from . import codes


class Spinner:
    FRAMES = [
        codes.TL_CODE,
        codes.T_CODE,
        codes.TR_CODE,
        codes.BR_CODE,
        codes.B_CODE,
        codes.BL_CODE
    ]
    CYCLES_PER_SECOND = 2

    def __init__(self, renderer):
        self.r = renderer
        self.frame = 0
        self.location = None
        self.enabled = True

    def start(self, row, column):
        if not self.location:
            self.t0 = int(time.time()/1000)
            self.location = (row, column)
            self.thread = Thread(target=self.spin)
            self.thread.daemon = True
            self.thread.start()

    def stop(self):
        if self.location:
            self.location = None
            self.thread.join()

    def render(self):
        if self.location and self.enabled:
            with self.r.location(self.location):
                self.r.write(self.FRAMES[self.frame])

    def step(self):
        t1 = int(time.time()*1000)
        if t1 - self.t0 > 1000/self.CYCLES_PER_SECOND/len(self.FRAMES):
            self.frame = (self.frame + 1) % len(self.FRAMES)
            self.t0 = t1

    def spin(self):
        while self.location:
            self.step()
            self.render()
            time.sleep(1/self.CYCLES_PER_SECOND/8)

    @contextmanager
    def disable(self):
        self.enabled = False
        # TODO: Oooh boy. What a hack. There are issues in screen
        # writes if I remove this delay.
        # time.sleep(0.01)
        try:
            yield
        finally:
            self.enabled = True

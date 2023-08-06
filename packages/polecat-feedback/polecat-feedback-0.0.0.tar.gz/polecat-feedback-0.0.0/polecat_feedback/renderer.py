from contextlib import contextmanager

from blessed import Terminal

from . import codes
from .gutter_renderer import GutterRenderer
from .header_renderer import HeaderRenderer
from .notice_renderer import NoticeRenderer
from .spinner import Spinner
from .stats_renderer import StatsRenderer
from .utils import ansi_clean


class Renderer:
    def __init__(self, max_width=None):
        self.t = Terminal()
        self.w = min(self.t.width, max_width or 9999)
        self.h = self.t.height
        self.y, self.x = self.t.get_location()
        self.wh = 0
        self.spinner = Spinner(self)
        self.header_renderer = HeaderRenderer(self)
        self.gutter_renderer = GutterRenderer(self)
        self.notice_renderer = NoticeRenderer(self)
        self.stats_renderer = StatsRenderer(self)

    def __enter__(self):
        self._ctx = self.t.hidden_cursor()
        self._ctx.__enter__()

    def __exit__(self, *exc):
        self._ctx.__exit__(*exc)
        self.spinner.stop()

    def render(self, f, y=None):
        if not f.parent:
            self.render_top_level(f)
        else:
            self.render_nested(f, y)

    def render_top_level(self, f):
        with self.spinner.disable():
            self.move((0, 0))
            self.x = 0
            self.wh = 0
            self.render_nested(f)
            if f.status != f.INITIALISING:
                self.stats_renderer.render(f)

    def render_nested(self, f, y=None):
        self.header_renderer.render(f, y)
        for notice in f.notices:
            self.notice_renderer.render(f, notice)
        if f.status != f.INITIALISING:
            if not f.parent:
                for step in f.steps:
                    self.render(step, y=self.wh)
            elif f.step_index < len(f.steps) and f.parent.step_index == f.index:
                self.render_action(f, y)

    def render_action(self, f, y=None):
        if f.steps[f.step_index].status == f.DONE:
            return
        t = self.t
        action = f.steps[f.step_index].title
        string = (
            ' ' + t.bright_black(codes.VERTICAL_CODE) +
            '    ' + t.bright_white('>') + '  ' + action
        )
        self.writeln(string)

    def buffer_step_count(self, f):
        t = self.t
        c = f.step_index
        s = len(f.steps)
        return f'{c}/{s} ' + t.green(codes.COMPLETED_STEP_CODE)

    def buffer_notice_count(self, f, count=None):
        t = self.t
        n = count if count is not None else f.info_count
        return f'{n} ' + t.cyan(codes.NOTICE_CODE)

    def buffer_warning_count(self, f, count=None):
        t = self.t
        w = count if count is not None else f.warning_count
        return f'{w} ' + t.yellow(codes.WARNING_CODE)

    def transition_to_ready(self):
        t = self.t
        self.spinner.stop()
        t.move(self.h - 2, 0)

    def right_align(self, to_align, on_left='', filler=' ', offset=0):
        padding = self.w - len(ansi_clean(to_align)) - len(ansi_clean(on_left)) - offset
        return on_left + filler*padding + to_align

    @contextmanager
    def location(self, location):
        y = self.y + location[0] - 1
        x = location[1]
        with self.t.location(y=y, x=x):
            yield

    def move(self, location):
        y = self.y + location[0] - 1
        x = location[1]
        print(self.t.move(y, x), end='')

    def write(self, string):
        self.x += len(string)
        print(string, end='')

    def writeln(self, string):
        clear = ' '*(self.t.width - (self.x + len(string)))
        print(string + clear)
        self.x = 0
        self.wh += 1
        if self.wh + self.y > self.h:
            self.y -= 1

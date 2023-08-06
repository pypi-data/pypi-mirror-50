from . import codes
from .notice import INFO
from .utils import identity


class GutterRenderer:
    def __init__(self, renderer):
        self.r = renderer
        self.t = renderer.t

    def buffer_header_gutter(self, f, y=None):
        t = self.t
        gutter_color = self.get_gutter_color(f)
        if f.index < f.parent.step_index:
            ballot = t.green(codes.COMPLETED_STEP_CODE)
        elif f.index > f.parent.step_index:
            ballot = t.bright_black(codes.STEP_CODE)
        else:
            ballot = codes.STEP_CODE
        if f.index == f.parent.step_index:
            self.r.spinner.start((y or 0), 4)
        if f.index < len(f.parent.steps) - 1:
            edge = codes.FORK_CODE
        else:
            edge = codes.BOTTOM_CORNER_CODE
        return (
            ' ' + gutter_color(edge + codes.HORIZONTAL_CODE) +
            ' ' + ballot + ' '
        )

    def buffer_notice_gutter(self, f, notice):
        t = self.t
        color = t.cyan if notice.level == INFO else t.yellow
        code = codes.NOTICE_CODE if notice.level == INFO else codes.WARNING_CODE
        return ' ' + t.bright_black(codes.VERTICAL_CODE) + '    ' + color(code) + ' '

    def get_gutter_color(self, f):
        t = self.t
        gutter_color = identity
        if f.index > f.parent.step_index:
            gutter_color = t.bright_black
        return t.bright_black  # gutter_color

from . import codes


class HeaderRenderer:
    def __init__(self, renderer):
        self.r = renderer
        self.t = renderer.t

    def render(self, f, y=None):
        if f.status == f.INITIALISING:
            self.render_initialising(f)
        else:
            if f.previous_status == f.INITIALISING:
                self.r.spinner.stop()
            if not f.parent:
                self.render_toplevel(f)
            else:
                self.render_nested(f, y)

    def render_initialising(self, f):
        r = self.r
        t = self.t
        title = (
            '    ' + t.bold_blue(f.app_name) + ' ' + t.blue(f.version) + ' ' +
            t.bright_black(codes.DASHED_HORIZONTAL_CODE) +
            ' Initialising ...'
        )
        with r.location((0, 0)):
            r.writeln(title)
        r.spinner.start(0, 2)

    def render_toplevel(self, f):
        r = self.r
        t = self.t
        app = ' ' + t.bold_blue(f.app_name) + ' ' + t.blue(f.version)
        title = (
            ' ' + t.bright_black(codes.UPPER_CORNER_CODE + codes.HORIZONTAL_CODE) +
            ' ' + f.title + ' '
        )
        r.writeln(r.right_align(app, title, filler=t.bright_black(codes.HORIZONTAL_CODE)))

    def render_nested(self, f, y=None):
        r = self.r
        t = self.t
        stats = (
            ' ' +
            r.buffer_warning_count(f) + ' ' +
            r.buffer_notice_count(f) + ' '
        )
        title = r.gutter_renderer.buffer_header_gutter(f, y) + f.title + ' '
        r.writeln(r.right_align(stats, title, filler=t.bright_black(codes.DASHED_HORIZONTAL_CODE)))

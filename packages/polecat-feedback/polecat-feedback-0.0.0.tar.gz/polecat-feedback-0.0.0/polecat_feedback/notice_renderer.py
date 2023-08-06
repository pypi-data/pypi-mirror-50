class NoticeRenderer:
    def __init__(self, renderer):
        self.r = renderer
        self.t = renderer.t

    def render(self, f, notice):
        r = self.r
        timeout = f'{notice.timeout}'
        string = (
            r.gutter_renderer.buffer_notice_gutter(f, notice) + ' '
            + notice.message
        )
        r.writeln(string)

class StatsRenderer:
    def __init__(self, renderer):
        self.r = renderer
        self.t = renderer.t

    def render(self, f):
        r = self.r
        stats = (
            r.buffer_step_count(f) + ' ' +
            r.buffer_warning_count(f) + ' ' +
            r.buffer_notice_count(f)
        )
        r.writeln(r.right_align(stats, offset=1))

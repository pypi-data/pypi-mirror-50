from .notice import INFO, WARNING, Notice


class Feedback:
    INITIALISING = 'initialising'
    READY = 'ready'
    WORKING = 'working'
    DONE = 'done'

    def __init__(self, title=None, renderer=None, app_name=None, version=None, parent=None, index=None, status=INITIALISING):
        self.title = title
        self.app_name = app_name
        self.version = version
        self.parent = parent
        self.index = index
        self.step_index = 0
        self.declared_steps = set()
        self.steps = []
        self.notices = []
        self.previous_status = None
        self.status = status
        self.renderer = renderer
        self.render()

    def __call__(self, title):
        from .decorators import feedback as feedback_decorator
        return feedback_decorator(title, parent_feedback=self)

    @property
    def current_step(self):
        return self.steps[self.step_index]

    @property
    def info_count(self):
        return (
            sum(s.info_count for s in self.steps) +
            len([n for n in self.notices if n.level == INFO])
        )

    @property
    def warning_count(self):
        return (
            sum(s.warning_count for s in self.steps) +
            len([n for n in self.notices if n.level == WARNING])
        )

    def set_status(self, status):
        self.previous_status = self.status
        self.status = status
        self.render()

    def declare_steps(self, *args):
        self.steps.extend([
            Feedback(title, parent=self, renderer=self.renderer, index=ii, status=self.READY)
            for ii, title in enumerate(args)
        ])
        self.render()

    def next_step(self, step=None):
        if step is None:
            self.status = self.DONE
            self.step_index = min(self.step_index + 1, len(self.steps))
            self.render()
            return
        if not len(self.steps):
            self.steps.append(step)
            step.parent = self
            step.index = self.step_index
            step.renderer = self.renderer
            step.status = self.READY
        else:
            cur_step = self.steps[self.step_index]
            if cur_step.title == step.title:
                self.steps[self.step_index] = step
                step.parent = self
                step.index = self.step_index
                step.renderer = self.renderer
                step.status = self.READY
                self.previous_status = self.status
                self.status = self.READY
            elif self.step_index < len(self.steps) - 1:
                next_step = self.steps[self.step_index + 1]
                if next_step.title == step.title:
                    self.step_index += 1
                    self.steps[self.step_index] = step
                    step.parent = self
                    step.index = self.step_index
                    step.renderer = self.renderer
                    step.status = self.READY
                else:
                    self.step_index += 1
                    self.steps.insert(self.step_index, step)
                    step.parent = self
                    step.index = self.step_index
                    step.renderer = self.renderer
                    step.status = self.READY
            else:
                self.step_index += 1
                self.steps.insert(self.step_index, step)
                step.parent = self
                step.index = self.step_index
                step.renderer = self.renderer
                step.status = self.READY
        self.render()

    def add_notice(self, notice, step=None):
        self.notices.append(Notice(notice))
        self.render()

    def add_warning(self, notice, step=None):
        self.notices.append(Notice(notice, level=WARNING))
        self.render()

    def render(self):
        if self.parent:
            self.parent.render()
        elif self.renderer:
            self.renderer.render(self)

# from functools import wraps

from .feedback import Feedback

# from .utils import decorator_with_args


# @decorator_with_args
# def feedback(func, title=None):
#     @wraps(func)
#     def inner(*args, feedback=None, parent_feedback=None, renderer=None, **kwargs):
#         assert not (feedback and parent_feedback)
#         if feedback is None:
#             feedback = Feedback(title, renderer=renderer)
#         else:
#             if title:
#                 feedback.title = title
#         if parent_feedback:
#             parent_feedback.next_step(feedback)
#         return func(*args, feedback=feedback, **kwargs)
#     return inner


class feedback:
    def __init__(self, func_or_title=None, feedback=None, parent_feedback=None, renderer=None, app_name=None, version=None):
        self.func = None if isinstance(func_or_title, str) else func_or_title
        self.title = func_or_title if isinstance(func_or_title, str) else None
        self.feedback = feedback
        self.parent_feedback = parent_feedback
        self.renderer = renderer
        self.app_name = app_name
        self.version = version

    def __enter__(self):
        assert not (self.feedback and self.parent_feedback)
        fb = self.feedback
        if fb is None:
            fb = Feedback(self.title, renderer=self.renderer, app_name=self.app_name, version=self.version)
            self.feedback = fb
        else:
            if self.title:
                fb.title = self.title
        if self.parent_feedback:
            self.parent_feedback.next_step(fb)
        if self.renderer and not self.parent_feedback:
            self.renderer.__enter__()
        return fb

    def __exit__(self, *exc):
        if self.feedback:
            self.feedback.set_status(self.feedback.DONE)
        if not self.parent_feedback:
            self.feedback.next_step()
        if self.renderer and not self.parent_feedback:
            self.renderer.__exit__(*exc)

    def __call__(self, *args, **kwargs):
        if self.func is None:
            self.func = args[0]
            return self.inner
        else:
            return self.inner(*args, **kwargs)

    def inner(self, *args, feedback=None, parent_feedback=None, **kwargs):
        if feedback:
            self.feedback = feedback
        if parent_feedback:
            self.parent_feedback = parent_feedback
        fb = self.__enter__()
        try:
            return self.func(*args, feedback=fb, **kwargs)
        finally:
            if self.feedback:
                self.feedback.set_status(self.feedback.DONE)
            if not self.parent_feedback:
                self.feedback.next_step()

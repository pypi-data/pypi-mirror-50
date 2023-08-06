import time

from .feedback import Feedback
from .renderer import Renderer

renderer = Renderer(max_width=80)

with renderer.t.hidden_cursor():
    feedback = Feedback('Test operation', renderer=renderer, app_name='Polecat', version='v0.0.0')
    feedback.declare_steps('First step', 'Second step', 'Third step')
    # time.sleep(1)

    first_step = Feedback('First step')
    feedback.next_step(first_step)
    # time.sleep(1)

    second_step = Feedback('Second step')
    feedback.next_step(second_step)
    # time.sleep(1)

    extra_step = Feedback('In the middle')
    second_step.next_step(extra_step)
    time.sleep(1)

    third_step = Feedback('Third step')
    feedback.next_step(third_step)
    time.sleep(1)

    feedback.next_step()
    
    # feedback.add_step(Feedback('Second step'))
    # feedback.add_step(Feedback('Third step'))
    # first_step.add_notice('This is a notice.')

    # feedback.render()
    # time.sleep(1)

    # feedback.set_status(feedback.READY)
    # time.sleep(1)

    # feedback.steps[0].add_warning('A warning')
    # feedback.steps[0].add_notice('Oh, this is a notice')
    # time.sleep(1)

    # feedback.next_step()
    # time.sleep(1)

    # feedback.next_step()
    # time.sleep(1)

    # feedback.next_step()

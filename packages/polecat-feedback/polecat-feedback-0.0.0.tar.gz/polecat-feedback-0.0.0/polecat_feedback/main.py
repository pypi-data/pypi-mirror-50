from .feedback import Feedback
from .renderer import Renderer

feedback = Feedback()
feedback.add_step('First step')
feedback.add_step('Second step')
feedback.add_step('Third step')
feedback.add_notice('This is a notice.')
feedback.add_warning('This is a warning.')

renderer = Renderer(feedback)
renderer.render()

# from blessed import Terminal

# term = Terminal()
# oy = term.height - 4

# # print(' Building')
# # print(term.green('\u256d' + '\u2500'*75))
# # print(term.green('\u256d\u2500 ') + 'Building')
# print('Building       1/3 ' + term.green('\u2611') + ' 3 ' + term.green('\u24d8') + '  4 ' + term.yellow('\u26a0'))
# print('\u251c\u2500 ' + term.green('\u2611') + ' Initialise')
# print('\u251c\u2500 \u2610 Clean')
# print(term.bright_black('\u2502') + '  \u2570\u2500 Loading configuration from somewhere ...')
# print(term.bright_black('\u2570\u2500 \u2610 Compress'))

# # with term.location(y=oy):
# #     print('Line 1')

# # with term.location(y=oy):
# #     print('Line 4')

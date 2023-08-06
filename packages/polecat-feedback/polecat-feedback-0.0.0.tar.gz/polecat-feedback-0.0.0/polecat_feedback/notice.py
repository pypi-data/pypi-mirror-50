INFO = 'info'
WARNING = 'warning'


class Notice:
    def __init__(self, message, level=INFO, timeout=5):
        self.message = message
        self.level = level
        self.timeout = timeout

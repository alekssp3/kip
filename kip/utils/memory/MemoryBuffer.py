class MemoryBuffer:
    def __init__(self, *args, **kwargs):
        self.buffer = []
        self.index = []
        self.buffer_size = 32
        self.circle_buffer = True


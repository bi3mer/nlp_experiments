class RingBuffer():
    def __init__(self, buffer_limit):
        self.buffer_limit = buffer_limit
        self.buffer = []

    def add(self, value):
        if len(self.buffer) == self.buffer_limit:
            self.buffer.pop(0)

        self.buffer.append(value)

    def get(self, index):
        assert index >= 0
        assert index < len(self.buffer)
        assert index < self.buffer_limit

        return self.buffer[index]

    def full(self):
        return len(self.buffer) == self.buffer_limit

from collections import deque

class Inbox:
    def __init__(self):
        self.messages = deque()

    def add_message(self, message):
        self.messages.append(message)

    def get_message(self):
        if len(self.messages) > 0:
            return self.messages.popleft()
        else:
            return None
    
    def __len__(self):
        return len(self.messages)
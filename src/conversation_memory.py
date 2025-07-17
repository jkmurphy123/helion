class ConversationMemory:
    def __init__(self, max_length=10):
        self.history = []
        self.max_length = max_length

    def add_user_message(self, message):
        self.history.append({"role": "user", "content": message})
        self.trim()

    def add_assistant_message(self, message):
        self.history.append({"role": "assistant", "content": message})
        self.trim()

    def get(self):
        return self.history

    def trim(self):
        if len(self.history) > self.max_length:
            self.history = self.history[-self.max_length:]

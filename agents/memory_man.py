import json

class DQMemory:
    def __init__(self, path="dq_memory.json"):
        self.path = path
        try:
            with open(path, "r") as f:
                self.memory = json.load(f)
        except:
            self.memory = []

    def log(self, event):
        self.memory.append(event)
        with open(self.path, "w") as f:
            json.dump(self.memory, f, indent=2)

    def get_memory(self):
        return self.memory

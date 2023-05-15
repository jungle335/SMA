class Plan:
    actions = None

    def __init__(self):
        self.actions = []

    def remove(self):
        self.actions.pop(0)

    def add_Action(self, action):
        if action is None:
            raise ValueError("The action cannot be empty!")
        self.actions.append(action)

    def cancel_plan(self):
        self.actions = []
    
    def finish_plan(self):
        exit(0)

    def __str__(self):
        return "\n".join(str(action) for action in self.actions)
    
  
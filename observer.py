class Subject:
    def __init__(self):
        """Inits the class."""
        self.observers = []
        self.state = None

    def set_state(self, state):
        self.state = state
        self.notify_observers()

    def get_state(self):
        return self.state

    def attach(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        for o in self.observers:
            o.update()


class Observer:
    def __init__(self, subject):
        self.subject = subject
        self.subject.attach(self)

    def update(self):
        pass

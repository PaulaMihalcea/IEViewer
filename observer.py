# This is a basic, manual implementation of the Observer design pattern.


class Subject:
    """Subject class.

    Attributes:
        observers: A list of all registered observers.
        state: The current state of the Subject.
    """
    def __init__(self):
        """Inits the class."""
        self.observers = []
        self.state = None

    def set_state(self, state):
        """State setter."""
        self.state = state
        self.notify_observers()

    def get_state(self):
        """State getter."""
        return self.state

    def attach(self, observer):
        """Attaches new observers to the list."""
        self.observers.append(observer)

    def notify_observers(self):
        """Notifies all observers."""
        for o in self.observers:
            o.update()


class Observer:
    """Observer class.

    Attributes:
        subject: The subject which is being currently observed.
    """
    def __init__(self, subject):
        """Inits the class."""
        self.subject = subject
        self.subject.attach(self)

    def update(self):
        """Empty update function, meant to be overridden."""
        pass

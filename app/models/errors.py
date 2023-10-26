class DriverNotInitialized(Exception):
    def __init__(self, message="A webdriver not initialized"):
        self.message = message
        super().__init__(self.message)


class TextAreaNotFound(Exception):
    def __init__(self, message="Text area for sending prompts not found!"):
        self.message = message
        super().__init__(self.message)


class NoFreeModelFound(Exception):
    def __init__(self, message="No free model found in the pool"):
        self.message = message
        super().__init__(self.message)


class BtnNotFound(Exception):
    def __init__(self, message="Button bot found"):
        self.message = message
        super().__init__(self.message)


class NotFoundMessageByPrompt(Exception):
    def __init__(self, message="Not found message by prompt"):
        self.message = message
        super().__init__(self.message)


class NotFoundMessageById(Exception):
    def __init__(self, message="Not found message by Id"):
        self.message = message
        super().__init__(self.message)

class NotFoundMessageAfterPrompt(Exception):
    def __init__(self, message="Can't find our message after send the prompt."):
        self.message = message
        super().__init__(self.message)

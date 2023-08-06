class TestConventionError(Exception):
    def __init__(self, message, convention_mistakes):
        super().__init__(message)
        self.mistakes = convention_mistakes

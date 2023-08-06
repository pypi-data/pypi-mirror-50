class TestConventionError(Exception):
    def __init__(self, message, convention_mistakes):
        super().__init__(message)
        self.mistakes = convention_mistakes

class EmptySubmissionsException(Exception):
    def __init__(self):
        super().__init__('Empty or uninitialized submissions object. Use LoadSubmissions class to get submissions')

class ServerOrScraperException(Exception):
    def __init__(self):
        super().__init__("Server returned a non-2XX HTTP status code. Either the cookie provided is invalid or expired. Or there is an issue with the scraper or server.")

class RangeError(Exception):
    def __init__(self):
        super().__init__('Left argument of range should be less than or equal to the right')

class FilterException(Exception):
    def __init__(self):
        super().__init__('Atleast one valid filter should be supplied. Please recheck filter configurations.')

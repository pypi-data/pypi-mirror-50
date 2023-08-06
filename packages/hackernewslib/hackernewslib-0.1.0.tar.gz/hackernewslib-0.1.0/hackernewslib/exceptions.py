class HackernewslibException(Exception):
    pass


class InvalidItemContents(HackernewslibException):
    def __init__(self, data=None, errors=None):
        super(InvalidItemContents, self).__init__(
            "invalid item contents", data, errors)

        self.data = data
        self.errors = errors

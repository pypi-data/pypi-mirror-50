
__all__ = ["StringExt"]


class StringExt(str):

    def __init__(self, val: str):
        if not isinstance(val, str):
            raise TypeError("S must be a string. Now is {}".format(type(val)))
        self.val = val

    def is_empty(self):
        return self.val is None or self.val == ""



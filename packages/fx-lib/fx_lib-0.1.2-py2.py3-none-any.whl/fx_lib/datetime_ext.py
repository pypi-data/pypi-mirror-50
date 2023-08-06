import datetime

__all__ = ["Date"]


class Date(datetime.datetime):

    def __new__(cls, dt=datetime.datetime.today()):
        if not isinstance(dt, datetime.datetime):
            raise TypeError("Wrong type. Should be Datetime")
        self = datetime.datetime.__new__(cls, dt.year, dt.month, dt.day)
        self._dt = dt
        return self

    def to_string_YYYY_MM_DD(self):
        return self._dt.strftime("%Y-%m-%d")
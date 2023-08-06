from math import floor, log10


class Zu:
    @staticmethod
    def int_exponent(x):
        return floor(log10(abs(x)))

    @staticmethod
    def is_positive(x):
        return x == abs(x)

# from time import sleep
# from zest.src.xbrief.evo import wl, now, wtag
from datetime import datetime, timedelta, time


class Eta:
    def __init__(self):
        self.__base = datetime.now()
        self.__just = self.__base
        self.__chic = self.__base
        self.__grad = 0
        self.__life = None

    def __update_chic(self):
        self.__chic = datetime.now()
        self.__grad = int((self.__chic - self.__just).total_seconds() * 1000)
        self.__just = datetime.now()

    def __update_life(self):
        self.__chic = datetime.now()
        self.__life = int((self.__chic - self.__base).total_seconds() * 1000)

    def tag(self, tagval):
        if tagval == 'End':
            # wtag('self.life', self.life)
            ms_span = self.life
        else:  # Contains 'Ini','Lap'
            ms_span = self.grad
        return f'{tagval} {ms_span:>+6,d}ms'

    def ini(self, msg=''):
        self.__init__()
        print(f"[{self.chic}] [{self.tag('Ini')}] {msg}")

    def lap(self, msg=''):
        self.__update_chic()
        print(f"[{self.chic}] [{self.tag('Lap')}] {msg}")

    def end(self, msg='') -> object:
        self.__update_chic()
        print(f"[{self.chic}] [{self.tag('End')}] {msg}")

    @property
    def chic(self):
        tm = self.__chic.time()
        return f'{tm:%H:%M:%S}.{int(tm.microsecond/1000):03d}'

    @property
    def grad(self):
        """
        grad = chic - just
        millisecond as int
        stored value last calculated by __lap
        """
        return self.__grad

    @property
    def life(self):
        """
        grad = chic - just
        millisecond as int
        stored value last calculated by __life
        """
        self.__update_life()
        return self.__life

    # def __getattr__(self, item):
    #     return self.tag(str(item))

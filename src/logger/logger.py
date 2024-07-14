import logging


class Logger:
    def __init__(self):
        self._loger = logging.getLogger()

        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        handler.setFormatter(formatter)

        self._loger.addHandler(handler)

    @property
    def loger(self):
        return self._loger


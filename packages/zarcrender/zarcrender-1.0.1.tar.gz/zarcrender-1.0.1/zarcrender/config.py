from .constant import *


class Config:

    __keys = ['dbms', 'grid', 'keys', 'request', 'cursor']

    def __init__(self):
        self.dbms = dbms.SQL
        self.grid = grid.DATATABLES
        self.keys = keys.QUERYDICT
        self.request = request.NONE
        self.cursor = cursor.NONE

    def update_from_dict(self, keys={}):
        for _k in self.__keys:
            if _k in keys:
                setattr(self, _k, keys[_k])


cfg = Config()

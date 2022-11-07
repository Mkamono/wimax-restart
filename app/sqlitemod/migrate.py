from sqlitemod.base import BaseEngine
from sqlitemod.models import Base


class Migration(object):
    def __init__(self, datapath):
        self.e = BaseEngine(datapath).engine

    def status(self):
        Base.metadata.create_all(self.e)

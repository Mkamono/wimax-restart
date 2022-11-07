from sqlalchemy.orm import sessionmaker
from sqlitemod.base import BaseEngine


class BaseSession(BaseEngine):
    def __init__(self, datapath):
        super().__init__(datapath=datapath)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

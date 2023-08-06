import pymongo
import logging


class MongoDatabase:

    def __init__(self, address="localhost", port=27017, user="foo", password="bar", database_name=None):
        self._log = logging.getLogger(__name__)
        self._client = None
        pass

    def _connect(self, address="localhost", port=27017, user="foo", password="bar", database_name=None):
        self._client = pymongo.MongoClient(address, port)
        self._database = self._client[database_name]



class Collection:
    pass
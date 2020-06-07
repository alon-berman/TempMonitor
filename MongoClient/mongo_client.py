from pymongo import MongoClient


class MongoHandler:
    def __init__(self):
        self.__client = MongoClient(
            'mongodb://admin:admin123@ds215563.mlab.com:15563/?authSource=berman_monitoring&authMechanism=SCRAM-SHA-1&retryWrites=false')
        self.db = self.__client.berman_monitoring

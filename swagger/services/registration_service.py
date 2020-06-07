from MongoClient.mongo_client import MongoHandler

mongo_handler = MongoHandler()


def register(data):
    businesses = mongo_handler.db.businesses
    id = businesses.insert_one(data).inserted_id
    #TODO: start_monitoring()
    #TODO: watch dog and exception handling
import os
from MongoClient.mongo_client import MongoHandler

mongo_handler = MongoHandler()


def register(data):
    businesses_data = data
    businesses_data['business_debug_mode'] = os.environ.get('BUSINESS_DEBUG_MODE')
    businesses_data['is_monitored'] = False
    businesses = mongo_handler.db.businesses
    businesses.insert_one(businesses_data)

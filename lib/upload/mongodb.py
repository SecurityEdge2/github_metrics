from pymongo import MongoClient
from config import config

def upload_to_mongodb(timeline, db, coolections):
    mongodb_config = config['mongodb']
    client = MongoClient(mongodb_config['host'], mongodb_config['port'])
    db = client[db]
    mongo_timeline_collection = db[coolections]
    mongo_timeline_collection.delete_many({})
    mongo_timeline_collection.insert_many(timeline)


    return None
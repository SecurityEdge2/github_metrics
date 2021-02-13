from pymongo import MongoClient
from config import config

def upload_data_to_mongodb(timeline):
    mongodb_config = config['mongodb']
    client = MongoClient(mongodb_config['host'], mongodb_config['port'])
    db = client['wrt4']
    mongo_timeline_collection = db['wrt4_6']
    mongo_timeline_collection.insert_many(timeline)
    #mongo_timeline_collection.insert(timeline[1])
    #mongo_timeline_collection.insert(timeline[2])

    return None
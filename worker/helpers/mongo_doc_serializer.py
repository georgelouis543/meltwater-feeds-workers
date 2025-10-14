def individual_doc_serialize(mongo_doc) -> dict:
    mongo_doc["_id"] = str(mongo_doc["_id"])
    return mongo_doc

def list_mongo_collection_serialize(mongo_docs) -> list:
    return [
        individual_doc_serialize(mongo_doc) for mongo_doc in mongo_docs
    ]
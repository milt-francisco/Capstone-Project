from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, user, password, host, port, db, col):

        # Initialize Connection
        
        self.client = MongoClient('mongodb://%s:%s@%s:%d/%s?authSource=%s' % (user,password,host,port, db, db))
        self.database = self.client['%s' % (db)]
        self.collection = self.database['%s' % (col)]

# Insert information into the db
    def create(self, data):
        try:
            inserted = self.collection.insert_one(data)
            return True if inserted.inserted_id else False
        except Exception as e:
            print(f"Error inserting document: {e}")
            return False

# Read info in the db
    def read(self, query):
        try:
            current = self.collection.find(query)
            return list(current)
        except Exception as e:
            print(f"Error querying documents: {e}")
            return []
        
# Modify information in the db
    def update(self, query, update_data):
        try:
            update_result = self.collection.update_many(query, {'$set': update_data})
            return update_result.modified_count
        except Exception as e:
            print(f"Error updating documents: {e}")
            return 0 
        
# Remove information in the db
    def delete(self, query):
        try:
            delete_result = self.collection.delete_many(query)
            return delete_result.deleted_count
        except Exception as e:
            print(f"Error deleting documents: {e}")
            return 0
      

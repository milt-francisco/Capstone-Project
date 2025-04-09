from pymongo import MongoClient

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, user, password):
        
        # Connection Constants
        HOST = 'ec2-3-145-82-100.us-east-2.compute.amazonaws.com'
        PORT = 27017
        DB = 'AAC'
        COL = 'animals'

        # Initialize Connection
        self.client = MongoClient('mongodb://%s:%s@%s:%d/%s?authSource=%s' % (user,password, HOST, PORT, DB, DB))
        self.database = self.client['%s' % (DB)]
        self.collection = self.database['%s' % (COL)]

# Insert information
    def create(self, data):
        try:
            inserted = self.collection.insert_one(data)
            return True if inserted.inserted_id else False
        except Exception as e:
            print(f"Error inserting document: {e}")
            return False

# Read documents in database
    def read(self, query):
        try:
            current = self.collection.find(query)
            return list(current)
        except Exception as e:
            print(f"Error querying documents: {e}")
            return []
        
# Modify information in documents
    def update(self, query, update_data):
        try:
            update_result = self.collection.update_many(query, {'$set': update_data})
            return update_result.modified_count
        except Exception as e:
            print(f"Error updating documents: {e}")
            return 0 
        
# Remove a document
    def delete(self, query):
        try:
            delete_result = self.collection.delete_many(query)
            return delete_result.deleted_count
        except Exception as e:
            print(f"Error deleting documents: {e}")
            return 0
      

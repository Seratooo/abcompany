
from pymongo.mongo_client import MongoClient

def getConnection():
  uri = "mongodb+srv://Abubacar:9uNYkufktH3pzzhW@cluster0-abcompany.low1axk.mongodb.net/?retryWrites=true&w=majority"

  # Create a new client and connect to the server
  client = MongoClient(uri)

  # Send a ping to confirm a successful connection
  try:
      client.admin.command('ping')
      #print("Pinged your deployment. You successfully connected to MongoDB!")
      return client["ABCompany"]
  except Exception as e:
      print(e)

db = getConnection()

def CreateCollection(Name, pd_csv):
   
   db.create_collection(Name)
   
   mycollection = db[Name]
   data = pd_csv.to_dict(orient = "records")
   mycollection.insert_many(data)


def GetAllCollectionNames():
   return db.list_collection_names()

def GetCollectionByName(Name):
   mycollection = db[Name]
   all_results = mycollection.find()
   return list(all_results)


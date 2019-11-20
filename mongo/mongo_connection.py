import pymongo
from scraper import scraper
from bson.objectid import ObjectId


client = pymongo.MongoClient("mongodb://pranav_user:@cluster0-shard-00-00-rxhhi.mongodb.net:27017,cluster0-shard-00-01-rxhhi.mongodb.net:27017,cluster0-shard-00-02-rxhhi.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client['Football_Stats']
collection = db['Jerry_Rice_Stats']
print(collection)
week_stats = scraper.create_week_dictionary()
for week in week_stats:
	collection.insert_one( {"week": week, "stats": week_stats[week]} )

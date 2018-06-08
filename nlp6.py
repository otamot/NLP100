import redis
import json
import pymongo


def get_redis_connection() -> redis.client.StrictRedis:
    return redis.StrictRedis(host='localhost', port=6379, db=0)


def json_lines_to_dict(path):
    with open(path, 'r') as fr:
        for row in fr:
            yield json.loads(row)

def get_mongo_connection():
    client = pymongo.MongoClient('localhost', 27017)
    db = client.test_database
    return db


con = get_redis_connection()
db = get_mongo_connection()
collection = db.test_collection


def nlp60(path: str) -> None:
    for artist in json_lines_to_dict(path):
        if 'area' in artist.keys():
            con.set(artist['name'], artist['area'])
    return None



def nlp61(name: str) -> str:
    return con.get(name).decode()


def nlp62(area: str) -> int:
    return len([key.decode() for key in con.keys() if con.get(key).decode() == area])


def nlp64(path: str) -> None:
    for artist in json_lines_to_dict(path):
        collection.insert_one(artist)
    for i in ['name', 'aliases.name', 'tags.value', 'rating.value']:
        collection.create_index([(i, pymongo.ASCENDING)])
    return None


def nlp65(key: str, value: str):
    return [post for post in collection.find({key: value})]


def nlp66(key: str, value: str):
    return collection.find({key: value}).count()


def nlp67(name: str):
    return [post for post in collection.find({'aliases.name': name})]


def nlp68():
    return [post for post in collection.find({"tags.value": "dance"}).sort('rating.count', -1).limit(10)]


def nlp69(key: str, value: str):
    return [post for post in collection.find({key: value}).sort('rating.count', -1).limit(10)]


if __name__ == '__main__':
    # print(60, nlp60('artist.json'))
    # print(61, nlp61('임지용'))
    # print(62, nlp62('Japan'))
    # print(64, nlp64('artist.json'))
    # print(65, nlp65('name', 'Queen'))
    # print(66, nlp66('area', 'Japan'))
    # print(67, nlp67('Spoom'))
    # print(68, nlp68())
    print(69, nlp69("name", "Queen"))
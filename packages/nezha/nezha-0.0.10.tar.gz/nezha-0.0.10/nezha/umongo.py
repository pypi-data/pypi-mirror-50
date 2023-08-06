from typing import Mapping, List, Dict

from pymongo import MongoClient


def insert_one(data: Mapping,
               collection: str, db: str, host: str, port: int, username: str, password: str,
               authSource: str) -> None:
    with MongoClient(host=host,
                     port=port,
                     username=username,
                     password=password,
                     authSource=authSource,
                     maxPoolSize=1) as MgClient:
        MgClient[db][collection].insert_one(data)


def find(condition: Mapping,
         collection: str, db: str, host: str, port: int, username: str, password: str,
         authSource: str) -> List[Dict]:
    with MongoClient(host=host,
                     port=port,
                     username=username,
                     password=password,
                     authSource=authSource,
                     maxPoolSize=1) as MgClient:
        return MgClient[db][collection].find(condition)

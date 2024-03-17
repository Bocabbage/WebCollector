from pymongo import MongoClient
from typing import Optional
import mysql.connector
from mysql.connector import MySQLConnection
from configs import MongoDBConfig, MySQLConfig
from utils import singleton

@singleton
class MySQLHelper:
    def _init_client(self):
        self.mysql_conn = mysql.connector.connect(
        host=MySQLConfig['host'],
        user=MySQLConfig['user'],
        password=MySQLConfig['password'],
        database=MySQLConfig['database']
    )
    
    def __init__(self):
        self.mysql_conn: Optional[MySQLConnection] = None
        
    def connection(self) -> MySQLConnection:
        if self.mysql_conn is None or not self.mysql_conn.is_connected():
            self._init_client()
        return self.mysql_conn
    

@singleton
class MongodbHelper:
    def _init_client(self):
        self.mongo_client = MongoClient(MongoDBConfig['host'])
    
    def __init__(self):
        self.mongo_client: Optional[MongoClient] = None
        
    def client(self) -> MongoClient:
        if self.mongo_client is None:
            self.mongo_client = MongoClient(MongoDBConfig['host'])
        return self.mongo_client

mongo_client = MongodbHelper()
mysql_conn = MySQLHelper()

def get_mongo_client() -> MongoClient:
    return mongo_client.client()

def get_mysql_conn() -> MySQLConnection:
    return mysql_conn.connection()
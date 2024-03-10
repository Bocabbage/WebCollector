from grpc_utils.mikanani_grpc_pb2_grpc import MikananiServiceServicer
from grpc_utils.mikanani_grpc_pb2 import *
from grpc import ServicerContext, StatusCode as gRPCStatusCode
from configs import MongoDBConfig, MySQLConfig
from logger import LOGGER
from pymongo import MongoClient
from typing import Optional, List
import traceback
import mysql.connector
from mysql.connector import MySQLConnection

class MikananiSvcServicer(MikananiServiceServicer):
    mongo_client: Optional[MongoClient] = None
    mysql_conn = None
    
    @classmethod
    def _init_mongo_client(cls):
        cls.mongo_client: Optional[MySQLConnection] = MongoClient(MongoDBConfig['host'])
        
    @classmethod
    def _init_mysql_client(cls):
        cls.mysql_conn = mysql.connector.connect(
            host=MySQLConfig['host'],
            user=MySQLConfig['user'],
            password=MySQLConfig['password'],
            database=MySQLConfig['database']
        )

    @classmethod
    def _get_mongo_col_cursor(cls):
        if cls.mongo_client is None:
            cls._init_mongo_client()
        # TODO: Add timeout retry
        mongo_db = cls.mongo_client[MongoDBConfig['mikandb']]
        return mongo_db[MongoDBConfig['mikancollection']]
    
    @classmethod
    def _get_mysql_conn(cls):
        if cls.mysql_conn is None:
            cls._init_mysql_client()
        # TODO: Add timeout retry
        return cls.mysql_conn
    
    async def ListAnimeMeta(self, request: ListAnimeMetaRequest, context: ServicerContext):
        active_type_query_map = {
            0: "",                           # All
            1: "WHERE is_active is TRUE",    # Only active
            2: "WHERE is_active is FALSE",   # Only inactive
        }
        active_filter = active_type_query_map.get(request.statusFilter)
        if (active_filter is None or
            request.startIndex > request.endIndex or
            request.startIndex < -1 or request.endIndex < -1
        ):
            context.set_code(gRPCStatusCode.INVALID_ARGUMENT)
            context.set_details(f"invalid filter or active_type: "
                f"start-{request.startIndex}, end-{request.endIndex}, filter-{request.statusFilter}.")
            return ListAnimeMetaResponse()

        sql = ("SELECT uid, name, download_bitmap, is_active, tags "
                f"FROM `mikanani`.`anime_meta` {active_filter}")
        if request.startIndex != -1 or request.endIndex != -1:
            sql += f" LIMIT {request.startIndex - 1}, {request.endIndex - request.startIndex + 1};"
        meta_array: List[AnimeMeta] = list()
        result = list()
        try:
            conn = self._get_mysql_conn()
            cursor = conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                for uid, name, download_bitmap, is_active, tags in result:
                    meta_array.append(AnimeMeta(
                        uid=uid, 
                        name=name, 
                        downloadBitmap=download_bitmap, 
                        isActive=is_active, 
                        # tags=tags
                    ))
            LOGGER.debug(f"f[ListAnimeMeta][mysql] return {len(result)}")
        except Exception as e:
            LOGGER.error(f"[ListAnimeMeta] exception-{e}: {traceback.format_exc()}")
            context.set_code(gRPCStatusCode.INVALID_ARGUMENT)
            context.set_details("invalid filter or active_type.")
            return ListAnimeMetaResponse()
        
        LOGGER.debug(f"f[ListAnimeMeta][SUCCESS] return ({len(result)}, {meta_array[:1]}...)")
        return ListAnimeMetaResponse(itemCount=len(result), animeMetas=meta_array)
    
    async def GetAnimeDoc(self, request, context):
        return GetAnimeDocResponse()
    
    async def UpdateAnimeDoc(self, request: UpdateAnimeDocRequest, context:ServicerContext):
        return None
    
    async def UpdateAnimeMeta(self, request, context):
        return None
    
    async def InsertAnimeItem(self, request, context):
        return None
    
    async def DeleteAnimeItem(self, request, context):
        return None
    
    async def DispatchDownloadTask(self, request, context):
        return None
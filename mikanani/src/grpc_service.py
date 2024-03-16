from grpc_utils.mikanani_grpc_pb2_grpc import MikananiServiceServicer
from grpc_utils.mikanani_grpc_pb2 import *
from grpc import ServicerContext, StatusCode as gRPCStatusCode
from configs import MongoDBConfig, MySQLConfig
import db_helper
from bson.int64 import Int64
from dispatcher import MikanamiAnimeDispatcher
from logger import LOGGER
from pymongo import MongoClient
from typing import Optional, List
import traceback
from mysql.connector import MySQLConnection
from snowflake import SnowflakeGenerator

# TODO: enhance machine-id gathering
id_generator = SnowflakeGenerator(42)

def get_mongo_col_cursor():
    mongo_client = db_helper.get_mongo_client()
    mongo_db = mongo_client[MongoDBConfig['mikandb']]
    mongo_col = mongo_db[MongoDBConfig['mikancollection']]
    return mongo_col


class MikananiSvcServicer(MikananiServiceServicer):
    mongo_client: Optional[MongoClient] = None
    mysql_conn: Optional[MySQLConnection] = None
    
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
                f"FROM `mikanani`.`anime_meta` {active_filter} ORDER BY uid")
        if request.startIndex != -1 or request.endIndex != -1:
            sql += f" LIMIT {request.startIndex - 1}, {request.endIndex - request.startIndex + 1};"
        meta_array: List[AnimeMeta] = list()
        result = list()
        try:
            conn = db_helper.get_mysql_conn()
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
            LOGGER.debug(f"[ListAnimeMeta][mysql] return {len(result)}")
        except Exception as e:
            LOGGER.error(f"[ListAnimeMeta] exception-{e}: {traceback.format_exc()}")
            context.set_code(gRPCStatusCode.INVALID_ARGUMENT)
            context.set_details("invalid filter or active_type.")
            return ListAnimeMetaResponse()
        
        LOGGER.debug(f"[ListAnimeMeta][SUCCESS] return ({len(result)}, {meta_array[:1]}...)")
        cursor.close()
        return ListAnimeMetaResponse(itemCount=len(result), animeMetas=meta_array)

    
    async def GetAnimeDoc(self, request: GetAnimeDocRequest, context: ServicerContext):
        uid = request.uid
        try:
            mongo_col = get_mongo_col_cursor()
            result = [x for x in mongo_col.find({"uid": Int64(uid)}, {"_id": 0})]
            LOGGER.debug(f"[GetAnimeDoc][return success] get uid-{uid} doc: {result}")
            if result:
                result = result[0]
                return GetAnimeDocResponse(
                    animeDoc=AnimeDoc(
                        uid=int(result["uid"]),
                        rssUrl=result["rss_url"],
                        rule=result["rule"],
                        regex=result["regex"],
                    ))
            else:
                return GetAnimeDocResponse(animeDoc=None)
        except Exception as e:
            LOGGER.error(f"[GetAnimeDoc][query_mongo] {e}[{traceback.format_exc()}]")
            context.set_code(gRPCStatusCode.INTERNAL)
            context.set_details(f"internal error when update mongodb.")
            return GetAnimeDocResponse()
        
    
    async def UpdateAnimeDoc(self, request: UpdateAnimeDocRequest, context:ServicerContext):
        try:
            uid = request.updateAnimeDoc.uid
            mongo_col = get_mongo_col_cursor()
            expected_update = {
                "rss_url": request.updateAnimeDoc.rssUrl,
                "rule": request.updateAnimeDoc.rule,
                "regex": request.updateAnimeDoc.regex,
            }
            # Remove no-change segment
            expected_update = {k:v for k, v in expected_update.items() if v}
            result = mongo_col.update_one(
                {"uid": Int64(uid)},
                {
                    "$set": expected_update,
                },
                upsert=False,
            )
            if result.upserted_id is None:
                LOGGER.warning(f"[UpdateAnimeDoc]upsert failed for uid[{uid}]: {expected_update}")
                context.set_code(gRPCStatusCode.INVALID_ARGUMENT)
                context.set_details(f"update failed.")
            else:
                LOGGER.info(f"[UpdateAnimeDoc][SUCCESS]: uid[{uid}]")
        except Exception as e:
            LOGGER.error(f"[UpdateAnimeDoc] {e}[{traceback.format_exc()}]")
            LOGGER.debug(f"[UpdateAnimeDoc][uid: {uid}][request: {request.updateAnimeDoc}]")
            context.set_code(gRPCStatusCode.INTERNAL)
            context.set_details(f"internal error when update mongodb.")
        return None
    
    async def UpdateAnimeMeta(self, request: UpdateAnimeMetaRequest, context: ServicerContext):
        try:
            uid = request.updateAnimeMeta.uid
            qsql = ("SELECT uid, name, download_bitmap, is_active, tags "
                    f"FROM `mikanani`.`anime_meta` WHERE uid = {uid};")
            conn = db_helper.get_mysql_conn()
            cursor = conn.cursor()
            cursor.execute(qsql)
            result = cursor.fetchall()
            if result:
                _, name, download_bitmap, is_active, tags = result[0]
                #TODO generize
                name = request.updateAnimeMeta.name if request.updateAnimeMeta.name is not None else name
                download_bitmap = request.updateAnimeMeta.downloadBitmap if request.updateAnimeMeta.downloadBitmap is not None else download_bitmap
                is_active = request.updateAnimeMeta.isActive if request.updateAnimeMeta.isActive is not None else is_active
                
                usql = ("UPDATE `mikanani`.`anime_meta` "
                        f"SET name = {name}, "
                        f"download_bitmap = {download_bitmap} "
                        f"is_active = {is_active} " 
                        f"WHERE uid = {uid};")
                cursor.execute(usql)
                conn.commit()
                if cursor.rowcount != 1:
                    context.set_code(gRPCStatusCode.INVALID_ARGUMENT)
                    context.set_details(f"anime update failed.")
                    conn.rollback()
                    cursor.close()
                    return None
                else:
                    LOGGER.info(f"[UpdateAnimeMeta][SUCCESS]: uid[{uid}]")
            else:
                context.set_code(gRPCStatusCode.INVALID_ARGUMENT)
                context.set_details(f"anime not exist.")
                LOGGER.debug(f"[UpdateAnimeMeta] anime not exist: uid[{uid}], request[{request.updateAnimeMeta}]")
                cursor.close()
                return None
        except Exception as e:
            conn.rollback()
            LOGGER.error(f"[UpdateAnimeMeta][uid: {uid}][request: {request.updateAnimeMeta}] {e}[{traceback.format_exc()}]")
            context.set_code(gRPCStatusCode.INTERNAL)
            context.set_details(f"internal error when update meta.")
        cursor.close()
        return None


    async def InsertAnimeItem(self, request: InsertAnimeItemRequest, context: ServicerContext):
        try:
            uid = next(id_generator)
            meta_info = request.insertAnimeMeta
            doc_info = request.insertAnimeDoc

            # Insert meta into mysql
            mysql_conn = db_helper.get_mysql_conn()
            cursor = mysql_conn.cursor()
            isql = ("INSERT INTO `mikanani`.`anime_meta` (uid, name, is_active) "
                    f"VALUES ({uid}, '{meta_info.name}', TRUE);")
            cursor.execute(isql)
            mysql_conn.commit()

            # Insert doc into mongodb
            mongo_client = db_helper.get_mongo_client()
            with mongo_client.start_session() as session:
                with session.start_transaction():
                    mongo_col = get_mongo_col_cursor()
                    mongo_col.insert_one({
                        "uid": Int64(uid),
                        "rss_url": doc_info.rssUrl,
                        "rule": doc_info.rule,
                        "regex": doc_info.regex,
                    }, session=session)

        except Exception as e:
            mysql_conn.rollback()
            LOGGER.error(f"[InsertAnimeItem][name: {meta_info.name}] {e}: {traceback.format_exc()}")
            context.set_code(gRPCStatusCode.INTERNAL)
            context.set_details("insert failed.")
        return None

    
    async def DeleteAnimeItem(self, request: DeleteAnimeItemRequest, context: ServicerContext):
        uid = request.uid
        try:
            conn = db_helper.get_mysql_conn()
            cursor = conn.cursor()
            dsql = f"DELETE FROM `mikanani`.`anime_meta` WHERE uid = {uid}"
            cursor.execute(dsql)
            conn.commit()
            
            if cursor.rowcount > 0:
                LOGGER.info(f"[DeleteAnimeItem][delete {uid} from meta-table.")
                mongo_col = get_mongo_col_cursor()
                result = mongo_col.delete_one({"uid": Int64(uid)})
                if result.deleted_count != 1:
                    LOGGER.warning(f"[DeleteAnimeItem]delete {result.deleted_count} for uid [{uid}].")
                    context.set_code(gRPCStatusCode.INVALID_ARGUMENT)
                    context.set_details(f"delete failed.")
                else:
                    LOGGER.info(f"[DeleteAnimeItem][SUCCESS]: uid[{uid}]")
            else:
                context.set_code(gRPCStatusCode.INVALID_ARGUMENT)
                context.set_details("anime item not exist.")
            
        except Exception as e:
            LOGGER.error(f"[DeleteAnimeItem] {e}[{traceback.format_exc()}]")
            context.set_code(gRPCStatusCode.INTERNAL)
            context.set_details(f"internal error when delete animeitem.")
        cursor.close()
        return None
    
    async def DispatchDownloadTask(self, request, context: ServicerContext):
        try:
            MikanamiAnimeDispatcher().sqs_dispatch()
        except Exception as e:
            LOGGER.error(f"[DispatchDownloadTask] {e}[{traceback.format_exc()}]")
            context.set_code(gRPCStatusCode.INTERNAL)
            context.set_details(f"internal error when dispatch download task.")
        return None

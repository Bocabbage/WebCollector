import traceback
from grpc import ServicerContext, StatusCode as gRPCStatusCode
from grpc_utils.mongodb_crud_pb2 import *
from grpc_utils.mongodb_crud_pb2_grpc import MikananiMongoCrudServicer
from typing import List
from pymongo import MongoClient
from bson.objectid import ObjectId
from logger import LOGGER
from mikanani.src.configs import MongoDBConfig

class MikananiMongoDBCrud(MikananiMongoCrudServicer):
    r'''
        AnimeDoc schema
        {
            _id
            name
            isActive
            rssVersion
            rssRegex
            isActive
        }
    '''
    @staticmethod
    def _get_col_cursor():
        mongo_client = MongoClient(MongoDBConfig['host'])
        mongo_db = mongo_client[MongoDBConfig['mikandb']]
        return mongo_db[MongoDBConfig['mikancollection']]


    async def QueryAnime(self, request: QueryAnimeRequest, context: ServicerContext) -> QueryAnimeResponse:
        result: List[dict] = list()

        active_type_query_map = {
            0: {},                      # All
            1: { "isActive": True },    # Only active
            2: { "isActive": False }    # Only inactive
        }

        names: List[str] = request.names
        active_type: int = request.activeType

        if (not names or 
            active_type < 0 or 
            active_type > max(active_type_query_map.keys())
        ):
            context.set_code(gRPCStatusCode.INVALID_ARGUMENT)
            context.set_details("invalid names or active_type.")
            return QueryAnimeResponse()
        
        query = active_type_query_map[active_type]
        try:
            if not (len(names) == 1 and names[0] == '*'):
                filter_cond = { "name": { "$in": names } }
                query = { "$and": [filter_cond, query] }
            LOGGER.info(f"[QueryAnime] query use - {query}")
        except Exception as e:
            LOGGER.error(f"[QueryAnime][buildquery] exception-{e}: {traceback.format_exc()}")
            context.set_code(gRPCStatusCode.INVALID_ARGUMENT)
            context.set_details(f"failed to build the query expr.")
            return QueryAnimeResponse()

        try:
            mongo_col = self._get_col_cursor()
            result = [x for x in mongo_col.find(query)]
        except Exception as e:
            LOGGER.error(f"[QueryAnime][querymongo] exception-{e}: {traceback.format_exc()}")
            context.set_code(gRPCStatusCode.INTERNAL)
            context.set_details(f"internal error when querying mongodb.")
            return QueryAnimeResponse()

        return QueryAnimeResponse(
            ids=[int(x["_id"]) for x in result],
            names=[x["name"] for x in result],
            rssUrl=[x["rss_url"] for x in result],
        )


    async def UpdateAnime(self, request: UpdateAnimeRequest, context: ServicerContext):
        ids: List[int] = request.ids
        names: List[str] = request.names
        rssUrls: List[str] = request.rssUrls
        rssVersions: List[str] = request.rssVersions
        rssRegexs: List[str] = request.rssRegexs
        isActives: List[bool] = request.isActives

        doc_num = len(ids)
        for x in [names, rssUrls, rssVersions, rssRegexs, isActives]:
            if len(x) != doc_num:
                context.set_code(gRPCStatusCode.INVALID_ARGUMENT)
                context.set_details("params num not consistent.")
                return UpdateAnimeResponse()
        successCount = 0
        failedList: List[str] = list()

        try:
            mongo_col = self._get_col_cursor()
            for idx, id in enumerate(ids):
                result = mongo_col.update_one(
                    {"_id": ObjectId(id)},
                    {
                        "$set": {
                            "name": names[idx],
                            "rssUrl": rssUrls[idx],
                            "rssVersion": rssVersions[idx],
                            "rssRegex": rssRegexs[idx],
                            "isActive": isActives[idx],
                        }
                    },
                    upsert=True,
                )
                if result.upserted_id is not None:
                    successCount += 1
                else:
                    LOGGER.warning(f"[UpdateAnime][update] {names[idx]} update/insert failed.")
        except Exception as e:
            LOGGER.error(f"[UpdateAnime][update] exception-{e}: {traceback.format_exc()}")
            context.set_code(gRPCStatusCode.INTERNAL)
            context.set_details(f"internal error when update mongodb.")
            return UpdateAnimeResponse()

        return UpdateAnimeResponse(
            successCount=successCount, 
            failedList=failedList
        )


    async def DelAnime(self, request: DelAnimeRequest, context: ServicerContext) -> DelAnimeResponse:
        delAll: bool = request.delAll
        ids: List[int] = request.ids
        successCount = 0

        try:
            mongo_col = self._get_col_cursor()
            if delAll:
                successCount = mongo_col.delete_many({}).deleted_count
            else:
                successCount = mongo_col.delete_many({ "_id": { "$in": [ObjectId(x) for x in ids] } })
        except Exception as e:
            LOGGER.error(f"[DelAnime][del] exception-{e}: {traceback.format_exc()}")
            context.set_code(gRPCStatusCode.INTERNAL)
            context.set_details(f"internal error when deleting records mongodb.")
            return DelAnimeResponse()

        return DelAnimeResponse(successCount=successCount)
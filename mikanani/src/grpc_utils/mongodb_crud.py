from grpc import ServicerContext, StatusCode as gRPCStatusCode
from mongodb_crud_pb2 import *
from mongodb_crud_pb2_grpc import MikananiMongoCrudServicer
from enum import Enum
from typing import List
from pymongo import MongoClient
from mikanani.src.configs import MongoDBConfig

class MikananiMongoDBCrud(MikananiMongoCrudServicer):
    @staticmethod
    def _get_col_cursor():
        mongo_client = MongoClient(MongoDBConfig['host'])
        mongo_db = mongo_client[MongoDBConfig['mikandb']]
        return mongo_db[MongoDBConfig['mikancollection']]

    async def QueryAnime(self, request: QueryAnimeRequest, context: ServicerContext):
        result: List[dict] = list()
        # [debug] test code
        names: List[str] = request.names
        # active_type: int = request.activeType
        return QueryAnimeResponse(
            names=names,
            rssUrl=[f"mockRssUrl{idx}" for idx, _ in enumerate(names)]
        )


        # active_type_query_map = {
        #     0: {},
        #     1: { "isActive": True },
        #     2: { "isActive": False }
        # }

        # names: List[str] = request.names
        # active_type: int = request.activeType

        # if (not names or 
        #     active_type < 0 or 
        #     active_type > max(active_type_query_map.keys())
        # ):
        #     context.set_code(gRPCStatusCode.INVALID_ARGUMENT)
        #     context.set_details("invalid names or active_type.")
        #     return QueryAnimeResponse()
        
        # query = active_type_query_map[active_type]
        # mongo_col = self._get_col_cursor()
        # if len(names) == 1 and names[0] == '*':
        #     result = [x for x in mongo_col.find(query, {"_id": 0})]
        # else:
        #     # TODO: serach name-list
        #     pass
        
        # return QueryAnimeResponse(
        #     names=[x["name"] for x in result],
        #     rssUrl=[x["rss_url"] for x in result],
        # )
    
    async def UpdateAnime(self, request: UpdateAnimeRequest, context: ServicerContext):
        # TODO: impl
        return UpdateAnimeResponse(
            successCount=0,
        )
    
    async def DelAnime(self, request: DelAnimeRequest, context: ServicerContext):
        # TODO: impl
        return DelAnimeResponse(
            successCount=0,
        )
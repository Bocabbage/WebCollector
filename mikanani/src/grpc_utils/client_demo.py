import grpc
import grpc_utils.mongodb_crud_pb2 as mongodb_crud_pb2
import grpc_utils.mongodb_crud_pb2_grpc as mongodb_crud_pb2_grpc

def test_query():
    channel = grpc.insecure_channel("localhost:50051")
    stub = mongodb_crud_pb2_grpc.MikananiMongoCrudStub(channel)
    request = mongodb_crud_pb2.QueryAnimeRequest(
        names=["*"],
        activeType=1
    )
    response = stub.QueryAnime(request)
    print(f"response: {response}")
    
def test_update():
    channel = grpc.insecure_channel("localhost:50051")
    stub = mongodb_crud_pb2_grpc.MikananiMongoCrudStub(channel)
    request = mongodb_crud_pb2.UpdateAnimeRequest(
        names=["test_mock_anime"],
        rssUrls=["testUrl"],
        ruleVersions=["latest"],
        ruleRegexs=["mock_regex"],
        isActives=[0]
    )
    response = stub.UpdateAnime(request)
    print(f"response: {response}")
    
def test_delete():
    channel = grpc.insecure_channel("localhost:50051")
    stub = mongodb_crud_pb2_grpc.MikananiMongoCrudStub(channel)
    request = mongodb_crud_pb2.DelAnimeRequest(
        delAll=False,
        names=["test_mock_anime"]
    )
    response = stub.DelAnime(request)
    print(f"response: {response}")

if __name__ == '__main__':
    # test_query()
    test_update()
    # test_delete()
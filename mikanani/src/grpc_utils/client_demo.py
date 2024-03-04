import grpc
import mongodb_crud_pb2
import mongodb_crud_pb2_grpc

def test_query():
    channel = grpc.insecure_channel("[::]:50051")
    stub = mongodb_crud_pb2_grpc.MikananiMongoCrudStub(channel)
    request = mongodb_crud_pb2.QueryAnimeRequest(
        names=["hello1", "hello2", "hello3", "hello4"],
        activeType=1
    )
    response = stub.QueryAnime(request)
    print(f"response: {response}")

if __name__ == '__main__':
    test_query()
# WebCollector

## Mikanani
Anime-downloader based on MikanAni-RSS subscription and Qbittorrent.
### gRPC-related
```shell
python -m grpc_tools.protoc \
-I./mikanani/protos \
--python_out=./mikanani/src/grpc \
--pyi_out=./mikanani/src/grpc \
--grpc_python_out=./mikanani/src/grpc \
./mikanani/protos/mongodb_crud.proto
```
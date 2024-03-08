# WebCollector

## Mikanani
Anime-downloader based on MikanAni-RSS subscription and Qbittorrent.
### gRPC-related
```shell
python -m grpc_tools.protoc \
-I./mikanani/protos \
--python_out=./mikanani/src/grpc_utils \
--pyi_out=./mikanani/src/grpc_utils \
--grpc_python_out=./mikanani/src/grpc_utils \
./mikanani/protos/mikanani_grpc.proto
```
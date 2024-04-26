# WebCollector

## Mikanani
Anime-downloader based on MikanAni-RSS subscription and Qbittorrent.
### gRPC-related
```shell
python -m grpc_tools.protoc \
-I./mikanani/protos \
-I ${GTPC_GATEWAY_THIRDPARTY_PATH} \
--python_out=./mikanani/src \
--pyi_out=./mikanani/src \
--grpc_python_out=./mikanani/src \
./mikanani/protos/mikanani_grpc.proto
```
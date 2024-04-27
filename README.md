# WebCollector

## Mikanani
Anime-downloader based on MikanAni-RSS subscription and Qbittorrent.
### gRPC-related
```shell
python -m grpc_tools.protoc \
-I./mikanani/protos \
-I ${GOPATH}/pkg/mod/github.com/grpc-ecosystem/grpc-gateway@v1.16.0/third_party/googleapis \
--python_out=./mikanani/src \
--pyi_out=./mikanani/src \
--grpc_python_out=./mikanani/src \
./mikanani/protos/mikanani_grpc.proto
```
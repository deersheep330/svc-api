# gRPC Service

#### create prototype
```
python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. api/protos/database.proto
```

#### start grpc server without docker
```
python start_grpc.py
```

#### run unittest for grpc server
```
python -m unittest api\client\database_client.py
```

#### start docker services
```
docker-compose build --no-cache
docker-compose push
docker stack deploy -c docker-compose.yml api
```

# create prototype
python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. api/protos/database.proto

# run unittest
python -m unittest api\client\database_client.py


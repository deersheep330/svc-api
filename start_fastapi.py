import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse

function_header_file_path = './api/protos/database_pb2_grpc.py'
struct_header_file_path = './api/protos/database_pb2.py'

app = FastAPI()

@app.get("/grpc/header/functions")
async def get_function_header_file():
    return FileResponse(function_header_file_path)

@app.get("/grpc/header/structs")
async def get_struct_header_file():
    return FileResponse(struct_header_file_path)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7654)

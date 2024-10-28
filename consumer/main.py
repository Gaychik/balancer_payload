from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import os
import argparse 
from aiohttp import ClientSession
import uvicorn

app = FastAPI()
class Message(BaseModel):
    body:str 
    image:bytes
    receiver:str

id_app=None
data=[]
parser = argparse.ArgumentParser()
parser.add_argument("--port",type=int,default=8000)
args = parser.parse_args()#Создается экземпляр класса Namespace



async def startup_task():
    global id_app
    async with ClientSession() as session:
        async with session.get("http://localhost:8000/subscribe",json={"host" : "localhost", "port": str(args.port)}) as response:
             data = await response.json()
             id_app = data['id_app']

app.add_event_handler("startup",startup_task)
    

            


@app.api_route("/", methods=["GET", "POST"])
def handler_traffic(msg:Message = None):
    data.append(msg)
    return JSONResponse(status_code=200, content={'message': f'connection established with the service_{id_app}'})


if __name__ == "__main__":
    uvicorn.run("main:app",port=args.port,reload=True)
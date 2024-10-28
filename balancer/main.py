from fastapi import FastAPI,Body,Depends
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from pydantic import BaseModel
import requests

class Message(BaseModel):
    body:str 
    image:bytes
    receiver:str

class Service(BaseModel):
    host:str 
    port:str

app = FastAPI()
services=[]


@app.get("/")
def main():
    return JSONResponse(status_code=200,content={"message":"Success connected!"})

pointer=0

@app.api_route("/traffic", methods=["GET", "POST"])
def handler_traffic(msg:Message = None):
    addr_service = services[pointer]
    if msg:
        response = requests.post(addr_service,json=msg.model_dump_json())
    else :
        response = requests.get(addr_service)
    pointer=(pointer+1)%len(services)
    return JSONResponse(response.status_code, content = response.json())



@app.get("/subscribe")
def subscribe(service:Service):
    services.append(":".join([service.host,service.port]))
    return JSONResponse(status_code=200,content={"result": "Ok","id_app":1234})





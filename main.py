import fnmatch
import os
import bios

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse


app = FastAPI()

hosts = []
db = {}

for root, dirnames, filenames in os.walk('/tmp/facts'):
    for filename in fnmatch.filter(filenames, '*.json'):
        hostname = filename.replace('.json', '')
        hosts.append(hostname)
        db[hostname] = bios.read(os.path.join(root, filename))


@app.get("/")
async def read_root():
    return JSONResponse(content={"message": "Welcome to this humble API."})


@app.get("/hosts")
async def read_hosts():
    return JSONResponse(content=hosts)


@app.get("/host/{hostname}")
async def read_host(hostname: str):
    if hostname in db:
        return JSONResponse(content=db[hostname])

    raise HTTPException(status_code=404, detail="Hostname not found")


@app.get("/host/{hostname}/{element}")
async def read_host_element(hostname: str, element: str):
    if hostname in db and element in db[hostname]:
        return JSONResponse(content=db[hostname][element])

    raise HTTPException(status_code=404, detail="Hostname or element not found")


if __name__ == "__main__":
    import uvicorn

    # Host and port where the API will be served
    host = "127.0.0.1"
    port = 9090

    uvicorn.run(app, host=host, port=port)

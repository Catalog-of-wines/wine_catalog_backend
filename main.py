# import uvicorn
#
# if __name__ == "__main__":
#     uvicorn.run("server.app:app", host="127.0.0.1", port=8000, reload=True)


from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

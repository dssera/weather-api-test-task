import uvicorn

from fastapi import FastAPI

from api.api_v1.endpoints.weather import router


app = FastAPI()
app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(host="0.0.0.0", port=80, app="main:app", reload=True)

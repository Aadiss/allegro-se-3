from fastapi import FastAPI
from .routers import core
from fastapi_pagination import add_pagination

app = FastAPI()

app.include_router(core.router)

add_pagination(app)
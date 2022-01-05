from fastapi import FastAPI
from .routers import core
from fastapi_pagination import add_pagination

tags_metadata = [
    {
        "name": "core",
        "description": "Core endpoints of the API. List repos, count stars and check languages popularity"
    }
]

app = FastAPI(openapi_tags=tags_metadata)

app.include_router(core.router)

add_pagination(app)
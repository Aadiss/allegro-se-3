from typing import List
from pydantic import BaseModel
from fastapi_pagination import Page


class UsernameSchema(BaseModel):
    username: str


class ReturnReposList(BaseModel):
    name: str
    stargazers_count: int


class ReturnStarsSum(BaseModel):
    stargazers_count_sum: int

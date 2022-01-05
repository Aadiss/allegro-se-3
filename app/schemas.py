from typing import List
from pydantic import BaseModel
from fastapi_pagination import Page


class UsernameSchema(BaseModel):
    username: str


class ReturnReposListSchema(BaseModel):
    name: str
    stargazers_count: int


class ReturnStarsSumSchema(BaseModel):
    stargazers_count_sum: int


class LanguageSizeSchema(BaseModel):
    language: str
    size: int

from typing import Optional
from pydantic import BaseModel
from fastapi_pagination import Page


class UsernameSchema(BaseModel):
    username: str
    token: Optional[str] = None


class ReturnReposListSchema(BaseModel):
    name: str
    stargazers_count: int


class ReturnStarsSumSchema(BaseModel):
    stargazers_count_sum: int


class LanguageSizeSchema(BaseModel):
    language: str
    size: int


class ReposNameSchema(BaseModel):
    name: str


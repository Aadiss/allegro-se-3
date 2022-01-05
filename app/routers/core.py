from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
import requests
from fastapi_pagination.links import Page
from fastapi_pagination import paginate

from .. import schemas


router = APIRouter(
    prefix='/core',
    tags=['core']
)


def _get_repos_by_username(username: str):
    try:
        response = requests.get(f'https://api.github.com/users/{username}/repos')
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


@router.get('/repos', status_code=status.HTTP_200_OK, response_model=List[schemas.ReturnReposList])
def get_repos(user: schemas.UsernameSchema):
    return _get_repos_by_username(user.username)


@router.get('/repos/pagination', status_code=status.HTTP_200_OK, response_model=Page[schemas.ReturnReposList])
def get_pagination_repos(user: schemas.UsernameSchema):
    return paginate(_get_repos_by_username(user.username))


@router.get('/repos/sum', status_code=status.HTTP_200_OK, response_model=schemas.ReturnStarsSum)
def get_stars_sum(user: schemas.UsernameSchema):
    listed_repos = [schemas.ReturnReposList(**repo) for repo in _get_repos_by_username(user.username)]

    return {"stargazers_count_sum": sum([repo.stargazers_count for repo in listed_repos])}

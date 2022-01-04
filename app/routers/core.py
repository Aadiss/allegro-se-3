from typing import List
from fastapi import APIRouter, HTTPException, status
import requests
from pydantic import parse_obj_as

from .. import schemas


router = APIRouter(
    prefix='/core',
    tags=['core']
)


@router.get('/repos', status_code=status.HTTP_200_OK, response_model=List[schemas.ReturnReposList])
def get_repos(user: schemas.UsernameSchema):
    try:
        response = requests.get(f'https://api.github.com/users/{user.username}/repos')
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


@router.get('/repos/sum', status_code=status.HTTP_200_OK, response_model=schemas.ReturnStarsSum)
def get_stars_sum(user: schemas.UsernameSchema):
    try:
        response = requests.get(f'https://api.github.com/users/{user.username}/repos')
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    listed_repos = [schemas.ReturnReposList(**repo) for repo in response.json()]

    return {"stargazers_count_sum": sum([repo.stargazers_count for repo in listed_repos])}

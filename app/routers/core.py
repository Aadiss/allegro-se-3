from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Depends
import requests
from fastapi_pagination.links import Page
from fastapi_pagination import paginate
import pandas as pd

from .. import schemas


router = APIRouter(
    prefix='/core',
    tags=['core']
)


def _get_repos_by_username(username: str, token: Optional[str] = None):
    res_list = []
    condition = True
    page = 1

    try:
        while condition:
            response = requests.get(f'https://api.github.com/users/{username}/repos?per_page=100&page={page}', headers={'Authorization': f"Bearer {token}"})
            if len(response.json()) < 100:
                condition = False
            res_list += response.json()
            page += 1
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return res_list


def _get_repo_languages(username: str, repo_name:str, token: Optional[str] = None):
    try:
        response = requests.get(f'https://api.github.com/repos/{username}/{repo_name}/languages', headers={'Authorization': f"Bearer {token}"})
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


@router.get('/repos', status_code=status.HTTP_200_OK, response_model=List[schemas.ReturnReposListSchema])
def get_repos(user: schemas.UsernameSchema):
    return _get_repos_by_username(user.username, user.token)


@router.get('/repos/pagination', status_code=status.HTTP_200_OK, response_model=Page[schemas.ReturnReposListSchema])
def get_pagination_repos(user: schemas.UsernameSchema):
    return paginate(_get_repos_by_username(user.username, user.token))


@router.get('/repos/sum', status_code=status.HTTP_200_OK, response_model=schemas.ReturnStarsSumSchema)
def get_stars_sum(user: schemas.UsernameSchema):
    listed_repos = [schemas.ReturnReposListSchema(**repo) for repo in _get_repos_by_username(user.username, user.token)]

    return {"stargazers_count_sum": sum([repo.stargazers_count for repo in listed_repos])}


@router.get('/repos/top-languages', status_code=status.HTTP_200_OK, response_model=List[schemas.LanguageSizeSchema])
def get_top_languages(user: schemas.UsernameSchema, top: int = None):
    listed_names = [schemas.ReposNameSchema(**repo) for repo in _get_repos_by_username(user.username, user.token)]
    listed_languages = [_get_repo_languages(user.username, repo.name, user.token) for repo in listed_names]

    df = pd.DataFrame(listed_languages)
    df = df.melt(var_name="language", value_name="size")
    df['size'] = df['size'].fillna(0)
    df = df.groupby('language', sort=True).sum().reset_index()
    df = df.sort_values(by=['size'], ascending=False)
    
    if top:
        return df.head(top).to_dict('r')
    
    return df.to_dict('r')
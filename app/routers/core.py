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
            if token:
                response = requests.get(f'https://api.github.com/users/{username}/repos?per_page=100&page={page}', headers={'Authorization': f"Bearer {token}"})
            else:    
                response = requests.get(f'https://api.github.com/users/{username}/repos?per_page=100&page={page}')
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
        if token:
            response = requests.get(f'https://api.github.com/repos/{username}/{repo_name}/languages', headers={'Authorization': f"Bearer {token}"})
        else:
            response = requests.get(f'https://api.github.com/repos/{username}/{repo_name}/languages')
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


@router.get('/repos/{username}', status_code=status.HTTP_200_OK, response_model=List[schemas.ReturnReposListSchema])
def get_repos(username: str, token: Optional[str] = None):
    return _get_repos_by_username(username, token)


@router.get('/repos/{username}/pagination', status_code=status.HTTP_200_OK, response_model=Page[schemas.ReturnReposListSchema])
def get_pagination_repos(username: str, token: Optional[str] = None):
    return paginate(_get_repos_by_username(username, token))


@router.get('/repos/{username}/sum', status_code=status.HTTP_200_OK, response_model=schemas.ReturnStarsSumSchema)
def get_stars_sum(username: str, token: Optional[str] = None):
    listed_repos = [schemas.ReturnReposListSchema(**repo) for repo in _get_repos_by_username(username, token)]

    return {"stargazers_count_sum": sum([repo.stargazers_count for repo in listed_repos])}


@router.get('/repos/{username}/top-languages', status_code=status.HTTP_200_OK, response_model=List[schemas.LanguageSizeSchema])
def get_top_languages(username: str, token: Optional[str] = None, top: int = None):
    if top:
        if top < 1:
            raise HTTPException(detail='top param has to be greater or equal to 1', status_code=status.HTTP_400_BAD_REQUEST)
    listed_names = [schemas.ReposNameSchema(**repo) for repo in _get_repos_by_username(username, token)]
    listed_languages = [_get_repo_languages(username, repo.name, token) for repo in listed_names]

    df = pd.DataFrame(listed_languages)
    df = df.melt(var_name="language", value_name="size")
    df['size'] = df['size'].fillna(0)
    df = df.groupby('language', sort=True).sum().reset_index()
    df = df.sort_values(by=['size'], ascending=False)
    
    if top:
        return df.head(top).to_dict('records')
    
    return df.to_dict('records')
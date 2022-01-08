from fastapi.testclient import TestClient
import os
from dotenv import load_dotenv

from .main import app

client = TestClient(app)

load_dotenv()


def test_get_all_repos_ok():
    response = client.get('/core/repos', json={"username":"aadiss", "token":os.getenv('ACCESS_TOKEN')})
    assert response.status_code == 200


def test_get_all_repos_error():
    response = client.get('/core/repos', json={"username":"xsajdaju123218sad@!@@", "token":os.getenv('ACCESS_TOKEN')})
    assert response.status_code == 404


def test_sum_stars_ok():
    response = client.get('/core/repos/sum', json={"username":"aadiss", "token":os.getenv('ACCESS_TOKEN')})
    assert response.status_code == 200
    assert response.json() == {"stargazers_count_sum": 0}


def test_sum_stars_allegro():
    response = client.get('/core/repos/sum', json={"username":"allegro", "token":os.getenv('ACCESS_TOKEN')})
    assert response.status_code == 200
    assert response.json()['stargazers_count_sum'] > 0


def test_sum_stars_error():
    response = client.get('/core/repos/sum', json={"username":"non_existing_usernane", "token":os.getenv('ACCESS_TOKEN')})
    assert response.status_code == 404


def test_sum_stars_calculate():
    response = client.get('/core/repos/sum', json={"username":"allegro", "token":os.getenv('ACCESS_TOKEN')})
    response_2 = client.get('/core/repos', json={"username":"allegro", "token":os.getenv('ACCESS_TOKEN')})
    assert response.status_code == 200
    assert response_2.status_code == 200
    stars_sum = sum([item['stargazers_count'] for item in response_2.json()])
    assert response.json()['stargazers_count_sum'] == stars_sum


def test_top_languages_all():
    response = client.get('/core/repos/top-languages', json={"username":"allegro"})
    assert response.status_code == 403


def test_top_languages_python():
    response = client.get('/core/repos/top-languages?top=1', json={"username":"aadiss", "token":os.getenv('ACCESS_TOKEN')})
    assert response.json()[0]['language'] == 'Python'


def test_top_languages_invalid_top():
    response = client.get('/core/repos/top-languages?top=-1', json={"username": "aadiss"})
    assert response.status_code == 400
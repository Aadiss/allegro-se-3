from fastapi.testclient import TestClient
import os
from dotenv import load_dotenv

from .main import app

client = TestClient(app)

load_dotenv()


def test_get_all_repos_ok():
    response = client.get(f'/core/repos/aadiss/sum?token={os.getenv("ACCESS_TOKEN")}')
    assert response.status_code == 200


def test_get_all_repos_error():
    response = client.get(f'/core/repos/xsajdaju123218sad@!@@?token={os.getenv("ACCESS_TOKEN")}')
    assert response.status_code == 404


def test_sum_stars_ok():
    response = client.get(f'/core/repos/aadiss/sum?token={os.getenv("ACCESS_TOKEN")}')
    assert response.status_code == 200
    assert response.json() == {"stargazers_count_sum": 0}


def test_sum_stars_allegro():
    response = client.get(f'/core/repos/allegro/sum?token={os.getenv("ACCESS_TOKEN")}')
    assert response.status_code == 200
    assert response.json()['stargazers_count_sum'] > 0


def test_sum_stars_error():
    response = client.get(f'/core/repos/non_existing_usernane/sum?token={os.getenv("ACCESS_TOKEN")}')
    assert response.status_code == 404


def test_sum_stars_calculate():
    response = client.get(f'/core/repos/allegro/sum?token={os.getenv("ACCESS_TOKEN")}')
    response_2 = client.get(f'/core/repos/allegro?token={os.getenv("ACCESS_TOKEN")}')
    assert response.status_code == 200
    assert response_2.status_code == 200
    stars_sum = sum([item['stargazers_count'] for item in response_2.json()])
    assert response.json()['stargazers_count_sum'] == stars_sum


def test_top_languages_all():
    response = client.get('/core/repos/allegro/top-languages')
    assert response.status_code == 403


def test_top_languages_python():
    response = client.get(f'/core/repos/aadiss/top-languages?top=1&token={os.getenv("ACCESS_TOKEN")}')
    assert response.json()[0]['language'] == 'Python'


def test_top_languages_invalid_top():
    response = client.get('/core/repos/aadiss/top-languages?top=-1')
    assert response.status_code == 400
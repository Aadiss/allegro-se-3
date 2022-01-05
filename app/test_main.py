from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_get_all_repos_ok():
    response = client.get('/core/repos', json={"username":"aadiss"})
    assert response.status_code == 200


def test_get_all_repos_error():
    response = client.get('/core/repos', json={"username":"xsajdaju123218sad@!@@"})
    assert response.status_code == 404


def test_sum_stars_ok():
    response = client.get('/core/repos/sum', json={"username":"aadiss"})
    assert response.status_code == 200
    assert response.json() == {"stargazers_count_sum": 0}


def test_sum_stars_allegro():
    response = client.get('/core/repos/sum', json={"username":"allegro"})
    assert response.status_code == 200
    assert response.json()['stargazers_count_sum'] > 0


def test_sum_stars_error():
    response = client.get('/core/repos/sum', json={"username":"non_existing_usernane"})
    assert response.status_code == 404


def test_sum_stars_calculate():
    response = client.get('/core/repos/sum', json={"username":"allegro"})
    response_2 = client.get('/core/repos', json={"username":"allegro"})
    assert response.status_code == 200
    assert response_2.status_code == 200
    stars_sum = sum([item['stargazers_count'] for item in response_2.json()])
    assert response.json()['stargazers_count_sum'] == stars_sum
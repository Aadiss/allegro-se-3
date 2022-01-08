# allegro-se-3
Jest to małe API stworzone za pomocą [FastAPI](https://www.google.com), które udostępnia kilka endpointów pozwalających na listowannie
wraz ze stronicowaniem repozytoriów danego użytkownika na GitHub, zliczanie sumy gwiazdek ze wszystkich repo oraz pozwala na wyświetlenie rankingu najpopularniejszych 
języków programowania użytych w projektach danego użytkownika. Całość została zrealizowana w oparciu o [API GitHuba](https://docs.github.com/en/rest).
---
# Dostęp publiczny
API dostępne jest na Google Cloud pod adresem:

https://allegro-se-3-ljuvv5sxjq-uc.a.run.app/docs

Do deploymentu użyto usługi Google Cloud Run

---
# Konfiguracja lokalna
## Docker
Najprostszym sposobem na lokalne postawienie aplikacji jest pobranie repo oraz przy użyciu konsoli w folderze, gdzie znajdują się pliki Dockera odpalić komendę:

> docker-compose up

To rozwiązanie wymaga zainstalowanego Dockera.

## Środowisko wirtualne
Kolejnym sposobem jest utowrzenie środowiska wirtualnego w dowolnym folderze roboczym za pomocą komendy:

> python3 -m venv [virtualenv_name]

Następnie aktywowanie go:

> MacOS: source [virtualenv_name]/bin/activate

> Windows: [virtualenv_name]\Scripts\activate

Przy aktywnym środowisku wirtualnym należy doinstalować zależności (w terminalu otwarty folder zawierający requirements.txt):

> pip install -r requirements.txt

Po pomyślnym zainstalowaniu zależności można odpalić aplikację przy użyciu uvicorn, przykładowo:

> uvicorn app.main:app --reload

## Testy
Na uruchomionym środowisku wirtualnym możliwe jest odpalenie testów poleceniem:

> pytest

Należy stowrzyć plik .env w folderze z testami, w którym powinien znaleźć się ACCESS_TOKEN pozwalający na nieograniczone requesty do API GitHuba:

> ACCESS_TOKEN=your_access_token
# Dokumentacja
***UWAGA API GitHuba dopuszcza pewien limit requestów bez uwierzytelniania, żeby spokojnie korzystać z API należy przekazywać acces token jako parametr ścieżki w postaci token=ACCESS_TOKEN. 
W celu pozyskania tokenu należy mieć konto na GitHub oraz odwiedzić ten [link](https://github.com/settings/tokens).***

## Listowanie repozytoriów na podstawie nazwy użytkownika
Zwraca wszystkie publiczne repozytoria danego użytkownika bez stronicowania. Opis stronicowania poniżej.
### URL: /core/repos/{username}
### Dozwolone metody: GET
### Przykładowe URL:
> /core/repos/allegro
### Przykładowy rezultat:
```json
[
  {
      "name": "akubra",
      "stargazers_count": 80
  },
  {
      "name": "allegro-api",
      "stargazers_count": 160
  },
  {
      "name": "allegro-tech-labs-iot",
      "stargazers_count": 1
  }
]
```
### Stronicowanie 
Zwraca repozytoria użytkownika wraz z możliwośią wyboru strony oraz maksymalnej ilości repozytoriów na stronie. W przypadku braku parametrów bazowo jest to
strona 1 o rozmiarze 50.
### URL: /core/repos/{username}/pagination     opcjonalnie: /core/repos/{username}/pagination?page=1&size=50
### Dozwolone metody: GET
### Przykładowy rezultat dla ścieżki: /core/repos/tiangolo/pagination?page=2&size=3&token=your_secret_token
```json
{
  "items": [
      {
          "name": "aiomysql",
          "stargazers_count": 0
      },
      {
          "name": "aiortc",
          "stargazers_count": 1
      },
      {
          "name": "alembic",
          "stargazers_count": 2
      }
  ],
  "total": 204,
  "page": 2,
  "size": 3,
  "links": {
      "first": "/core/repos/pagination?size=3&page=1",
      "last": "/core/repos/pagination?size=3&page=68",
      "self": "/core/repos/pagination?page=2&size=3",
      "next": "/core/repos/pagination?size=3&page=3",
      "prev": "/core/repos/pagination?size=3&page=1"
  }
}
```
## Sumowanie gwiazdek danego użytkownika
Zwraca obiekt json, w którym jest zawarta suma gwiazdek wszystkich publicznych repozytoriów danego użytkownika.
### URL: /core/repos/{username}/sum
### Dozwolone metody: GET
### Przykładowe URL:
> /core/repos/allegro/sum?token=your_secret_token
### Przykładowy rezultat:
```json
{
  "stargazers_count_sum": 14472
}
```
## Ranking najpopularniejszych języków programowania
Zwraca zadaną liczbę najpopularniejszych języków dla danego użytkownika na podstawie ilości bajtów kodu w nim napisanych. Można zdefiniować parametr top, który mówi ile topowych języków ma być zwróconych.
### URL: /core/repos/{username}/top-languages    opcjonalnie: /core/repos/{username}/top-languages?top=3
### Dozwolone metody: GET
### Przykładowe URL:
> /core/repos/allegro/top-languages?top=3&token=your_secret_token
### Przykładowy rezultat dla URL: /core/repos/top-languages?top=3
```json
[
  {
      "language": "Python",
      "size": 47464656
  },
  {
      "language": "HTML",
      "size": 25150863
  },
  {
      "language": "C++",
      "size": 24962275
  }
]
```
## Uwagi
### Do zrealizowania stronicowania użyto [FastAPI Pagination](https://github.com/uriyyo/fastapi-pagination)
### Do grupowania najpopularniejszych języków programowania użyto DataFrame'u z Pandas

# allegro-se-3
Jest to małe API stworzone za pomocą [FastAPI](https://www.google.com), które udostępnia kilka endpointów pozwalających na listowannie
wraz ze stronicowaniem repozytoriów danego użytkownika na GitHub, zliczanie sumy gwiazdek ze wszystkich repo oraz pozwala na wyświetlenie rankingu najpopularniejszych 
języków programowania użytych w projektach danego użytkownika. Całość została zrealizowana w oparciu o [API GitHuba](https://docs.github.com/en/rest).
---
# Dostęp publiczny
API dostępne jest na Google Cloud pod adresem:

adres

Oraz na Heroku:

adres
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

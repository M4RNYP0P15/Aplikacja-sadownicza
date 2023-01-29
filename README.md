# Strona sadownicza
Tworzy: 
>Grzegorz Kamil Marcińczyk

Aplikacja do zarządzania sądem.

## Umożliwia:
- przegląd różnych informacji odnośnie sadu np. pielęgnacja drzew 
- zakup roślin i środków wzmacniających 
- możliwość dodania drzewek/krzewów do listy posiadanych drzewek/krzewów:
 -
- 

## Wykorzystane narzędzia:
- Django
- PostgreSQL
- HTML, Bootstrap

## Aktorzy:
- użytkownik niezalogowany
- użytkownik zalogowany
- administrator

# Instalacja
Wymagany PostgreSQL
zmienna w path np.

```
setx /M path "%path%;C:\Program Files\PostgreSQL\15\bin"

```
### Tworzenie użytkownika, bazy, przyznawanie uprawnien
```
psql -U postgres

create user my_hero;create database my_db;alter role my_hero with password ‘zaqwsx’;grant all privileges on database my_db to my_hero;alter database my_db owner to my_hero;

```
```
git clone https://github.com/M4RNYP0P15/Aplikacja-sadownicza.git
```
```
cd .\Aplikacja-sadownicza\
```
```
python3 -m venv venv
```
Linux
```
source venv/bin/activate
```
Windows
```
venv\Scripts\activate.bat  lub venv\Scripts\activate
```
W przypadku błędu z uprawnieniami(Windows): 
```
Set-ExecutionPolicy RemoteSigned
```
Instalacja wymaganych bibliotek:
```
pip install -r requirements.txt
```
Usuwanie informacji o migracjach z bazą danych(można pominąć)
```
find . -path “*/migrations/*.py” -not -name “__init__.py” -deletefind . -path “*/migrations/*.pyc” -delete
```
Aktualizowanie bazy danych z modelami:(tworzenie/zmiana tabel w zależności od zmian w modelu)
```
python manage.py makemigrations
```
```
python manage.py migrate
```
Czyszczenie objektów oraz wczytywanie danych do bazy
```
python manage.py shell
from django.contrib.contenttypes.models import ContentType
ContentType.objects.all().delete()

python manage.py loaddata baza_danych.json
```
Tworzenie administratora(można pominąć):
```
python manage.py createsuperuser
```
Uruchomienie serwera
```
python manage.py runserver
```
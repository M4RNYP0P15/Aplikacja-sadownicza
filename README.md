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

```
git clone https://github.com/M4RNYP0P15/Aplikacja-sadownicza.git
```
```
cd event-calendar
```
```
python3 -m venv venv
```
```
source env/bin/activate
```
```
pip install -r requirements.txt
```
```
python manage.py makemigrations
```
```
python manage.py migrate
```
```
python manage.py createsuperuser
```
```
python manage.py runserver
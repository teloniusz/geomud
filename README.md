### GeoMUD - aplikacja do chodzenia po mapie

W podkatalogach można znaleźć opisy komponentów.

Główny katalog:

 * `compose.sh` - skrypt zastępujący uruchomienie `docker-compose` (wrapper). Przyjmuje te same
   argumenty, tworzy plik `.env`, jeśli go nie ma, zawierający losowe hasło do bazy PostGIS.
 * `docker-compose.yml` - specyfikacja serwisów.

## Uruchomienie

```./compose.sh up -d```

## Korzystanie

#. Aplikacja:
   ```telnet localhost 10023```
    (patrz też: dokumentacja w podkatalogu `mud/`)
#. Zarządzanie użytkownikami: `https://localhost:10443`
   (należy się spodziewać nieprawidłowego certyfikatu)

## Opis serwisów

#. Główny serwis - MUD

Multi User Dungeon - serwer telnet, który pozwala logującemu się chodzić
po rzeczywistych lokacjach pobranych z publicznych baz (dane w repozytorium
ograniczają lokacje do Polski). Dla lokacji można też pobrać informacje z wiki.

Aplikacja MUD używa serwisu Camel-Router jako backendu (routing komunikatów JSON),
również do autoryzacji.

#. Camel router
   Zapewnia routing i tłumaczenie komunikatów między pozostałymi serwisami i MUD.
#. Authserver
   Serwer OpenLDAP odpowiadający za użytkowników
#. LocDB
   Serwer PostGIS (Postgresql z rozszerzeniem GIS) odpowiadający za backend geolokalizacji - granice
   jednostek administracyjnych, położenie geograficzne i kierunki.
#. Locserver
   Aplikacja REST (python + Flask) serwująca dane z LocDB.
#. Wiki
   Aplikacja REST (python + Flask) serwująca dane z Wikipedii przez publiczne API

Domyślnie zestaw serwuje usługi na dwóch portach:

 * 10023 - usługa MUD (protokół telnet)
 * 10443 - usługa PHP LDAP Admin (zarządzanie użytkownikami)

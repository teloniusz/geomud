## GeoMUD - aplikacja do chodzenia po mapie

W podkatalogach można znaleźć opisy komponentów.

Główny katalog:

 * `compose.sh` - skrypt zastępujący uruchomienie `docker-compose` (wrapper). Przyjmuje te same
   argumenty, tworzy plik `.env`, jeśli go nie ma, zawierający losowe hasło do bazy PostGIS,
   skompiluje serwis *camel-router*, jeśli nie jest od razu skompilowany.
 * `docker-compose.yml` - specyfikacja serwisów.

### Wymagania

1. docker-compose i działający demon docker

2. Opcjonalnie: gradle (w miejscu wskazanym zmienną `$GRADLE_HOME`).
   Jeśli gradle nie będzie dostępne, skrypt `compose.sh` postara się go ściągnąć
   do katalogu tymczasowego, w celu użycia do kompilacji komponentu *camel-router*.

### Uruchomienie

```./compose.sh up -d```

Po wystartowaniu demona docker-compose warto uruchomić:

```docker-compose logs```

i odczekać przed korzystaniem do momentu, gdy wszystkie dane zostaną załadowane do bazy.

### Korzystanie

1. Aplikacja:
   ```telnet localhost 10023```
   (patrz też: dokumentacja w podkatalogu `mud/`)
   Domyślne dane użytkownika: scott/tiger
2. Zarządzanie użytkownikami: `https://localhost:10443`
   (należy się spodziewać nieprawidłowego certyfikatu)
   Domyślne dane administratora: patrz dokumentacja w katalogu `auth/`

### Opis serwisów

1. Główny serwis - `mud`
   Multi User Dungeon - serwer telnet, który pozwala logującemu się chodzić
   po rzeczywistych lokacjach pobranych z publicznych baz (dane w repozytorium
   ograniczają lokacje do Polski). Dla lokacji można też pobrać informacje z wiki.

   Aplikacja MUD używa serwisu Camel-Router jako backendu (routing komunikatów JSON),
   również do autoryzacji.
2. `camel-router`
   Zapewnia routing i tłumaczenie komunikatów między pozostałymi serwisami i MUD.
3. `authserver`
   Serwer OpenLDAP odpowiadający za użytkowników
4. `authadmin`
   Usługa PHPLdapAdmin do zarządzania serwerem OpenLDAP
5. `locdb`
   Serwer PostGIS (Postgresql z rozszerzeniem GIS) odpowiadający za backend geolokalizacji - granice
   jednostek administracyjnych, położenie geograficzne i kierunki.
6. `locserver`
   Aplikacja REST (python + Flask) serwująca dane z LocDB.
7. `wiki`
   Aplikacja REST (python + Flask) serwująca dane z Wikipedii przez publiczne API

Domyślnie zestaw serwuje usługi na dwóch portach:

 * 10023 - usługa MUD (protokół telnet)
 * 10443 - usługa PHP LDAP Admin (zarządzanie użytkownikami)

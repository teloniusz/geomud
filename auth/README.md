### Serwer autoryzacji - dane hierarchiczne

Katalog zawiera bazę dla hierarchii LDAP służącej do autoryzacji użytkowników MUDa.
Obraz kontenera pobiera dane z tej hierarchii podczas inicjalizacji bazy.

Dane tworzą hierarchię:
```
jnp2.mimuw.edu.pl
|--people
|    `--scott
`--groups
     `--authentication
          `--geomud
```

Użytkownik, żeby połączyć się z GeoMUD, musi się zautoryzować w jednostce *ou=people*
oraz należeć do grupy *ou=geomud,ou=authentication,ou=groups*.

W ramach aplikacji dostępny jest system zarządzania LDAP, **phpldapadmin**.
Docker-compose uruchamia go na porcie HTTPS 10443. Logować można się loginem
*cn=admin,dc=jnp2,dc=mimuw,dc=edu,dc=pl* oraz hasłem administratora widocznym
w `docker-compose.yml`.

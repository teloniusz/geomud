## GeoMUD - główna aplikacja

Aplikacja do "chodzenia po mapie".

W parametrze *mud.py* należy podać adres serwera odpowiadającego za routing (*camel-router*).

Sposób korzystania:

```
$ telnet localhost 10023
Trying ::1...
Connected to localhost.
Escape character is '^]'.
ÿûÿûÿü'ÿþÿýÿþÿýÿþ"ÿý'Username: scott
scott
Password: tiger

You are at Piątek, county: łęczycki, province: łódzkie
Available exits: n nne ene ese se sse ssw sw w wnw nnw
You have entered augmented text reality
Real Geo MUD: Piątek> info
info
 * Piątek: Piątek (skrót pt. lub piąt., symbol w kalendarzu Pt) – dzień tygodnia między czwartkiem a sobotą.
Według normy ISO-8601 jest piątym dniem tygodnia.
Real Geo MUD: Piątek>
```

Podstawowe polecenia:

 * `info`            - podaje dane z Wikipedii o bieżącym miejscu (jak widać, według nazwy)
 * `around`          - jak wyżej, według lokalizacji geograficznej, wiele stron
 * `loc`             - dane o miejscu, w którym się znajdujemy
 * `go <kierunek>`,
   `n`, `nnw`, `nw`, `e`, `s` i tak dalej
                     - pójście w danym kierunku na mapie, jeśli jest dostępny
 * `help`            - pomoc
 * `quit`, `Ctrl-D`  - zakończenie sesji

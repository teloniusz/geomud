### Serwer lokalizacji z bazą

Aplikacja python+Flask oferująca prosty interfejs REST
plus jej backend realizowany przez bazę PostGIS (Postgresql
z rozszerzeniami GIS do przeliczania kierunków i odległości
w ramach geolokalizacji).

W podkatalogu *sql/* znajdują się pliki inicjalizujące bazę:
*miejsca.sql* zawierające listę miejsc w Polsce (źródło: dane
lokalizacyjne UE, w podkatalogu *scripts/* jest skrypt, który
je ściąga) oraz *powiaty.sql* zawierające dane o granicach
powiatów ściągnięte z oficjalnych polskich źródeł urzędowych
(skonwertowane z bazy dbf).

Serwis REST oferuje:

 * znalezienie miejsca o danej nazwie lub ID
 * znalezienie sąsiadów danego miejsca w 16 możliwych kierunkach
 * określenie, do jakiego powiatu i województwa należy dany punkt

Moduły:

 * *backend.py* - bazowa klasa do modelu
 * *model.py* - model (komunikacja z bazą PostGIS)
 * *rest.py* - aplikacja MVC (a w zasadzie MC, zawiera kontrolery REST)

 Pozostałe pliki są wykorzystywane przez obraz uruchamiający Python/Flask.

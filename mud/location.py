from threading import Thread
import time

class Loc:
    N = 0
    NNE = 1
    NE = 2
    ENE = 3
    E = 4
    ESE = 5
    SE = 6
    SSE = 7
    S = 8
    SSW = 9
    SW = 10
    WSW = 11
    W = 12
    WNW = 13
    NW = 14
    NNW = 15

    DIRDATA = [
        {'name': 'north', 'short': 'n', 'dir': 0},
        {'name': 'north-northeast', 'short': 'nne', 'dir': 22.5},
        {'name': 'northeast', 'short': 'ne', 'dir': 45},
        {'name': 'east-northeast', 'short': 'ene', 'dir': 67.5},
        {'name': 'east', 'short': 'e', 'dir': 90},
        {'name': 'east-southeast', 'short': 'ese', 'dir': 112.5},
        {'name': 'southeast', 'short': 'se', 'dir': 135},
        {'name': 'south-southeast', 'short': 'sse', 'dir': 157.5},
        {'name': 'south', 'short': 's', 'dir': 180},
        {'name': 'south-southwest', 'short': 'ssw', 'dir': 202.5},
        {'name': 'southwest', 'short': 'sw', 'dir': 225},
        {'name': 'west-southwest', 'short': 'wsw', 'dir': 247.5},
        {'name': 'west', 'short': 'w', 'dir': 270},
        {'name': 'west-northwest', 'short': 'wnw', 'dir': 292.5},
        {'name': 'northwest', 'short': 'nw', 'dir': 315},
        {'name': 'north-northwest', 'short': 'nnw', 'dir': 337.5}
    ]

    DIRS = {}
    for idx, data in enumerate(DIRDATA):
        data['idx'] = idx
        DIRS[data['name']] = DIRS[data['short']] = data

    def __init__(self, locid, name, info='', location='', neighbors=None):
        self.locid = locid
        self.name = name
        self.info = info
        self.location = location
        self.neighbors = neighbors or {}
        self.subkey = self.locid / 3

    def add_neighbor(self, neighbor, direction):
        self.neighbors[self.DIRS[direction]['name']] = neighbor
        neighbor.neighbors[self.DIRDATA[(self.DIRS[direction]['idx'] + 8) % 16]['name']] = self



class LocationServer:
    def __init__(self):
        self.locations = {
            1: Loc(1, 'Warszawa'),
            2: Loc(2, 'Legionowo'),
            3: Loc(3, 'Piaseczno'),
            4: Loc(4, 'Piastów'),
            5: Loc(5, 'Łomianki'),
            6: Loc(6, 'Ożarów Maz'),
            7: Loc(7, 'Józefów')
        }
        self.locations[1].add_neighbor(self.locations[2], 'n')
        self.locations[1].add_neighbor(self.locations[3], 's')
        self.locations[1].add_neighbor(self.locations[4], 'wsw')
        self.locations[1].add_neighbor(self.locations[5], 'nnw')
        self.locations[1].add_neighbor(self.locations[6], 'w')
        self.locations[1].add_neighbor(self.locations[7], 'sse')
        self.locations[2].add_neighbor(self.locations[5], 'w')

    def get_neighbors(self, location):
        return location.neighbors


class Map:
    def __init__(self, url):
        self.url = url
        self.clients = {}
        self.locserver = LocationServer()
        self.start_location = self.locserver.locations[1]

        self.talker = Thread(target=self.handle_talk, daemon=True)
        self.talker.start()

    def add_client(self, client):
        self.clients[id(client)] = {
            'start': time.time(),
            'last': time.time(),
            'client': client,
            'location': client.location
        }

    def location_change(self, client):
        data = self.clients[id(client)]
        self.locserver.get_neighbors(data['client'].location)
        if data['location'].subkey != data['client'].location.subkey:


    def del_client(self, client):
        data = self.clients[id(client)]
        data['client'].writeresponse(f"\nFarewell - we've been together for {time.time() - data['start']} seconds")
        del self.clients[id(client)]

    def handle_talk(self):
        while True:
            time.sleep(5)
            now = time.time()
            for client in self.clients.values():
                if now - client['last'] > 60:
                    client['client'].writeresponse(f"\nA minute passed again")
                    client['last'] = now

import requests
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

    def __init__(self, server, loc_id, name, coords=None, county='', province='', neighbors=None):
        self.server = server
        self.loc_id = loc_id
        self.name = name
        self.coords = coords
        self.county = county
        self.province = province
        self.neighbors = neighbors
        self.last_update = time.time()

    def add_neighbor(self, neighbor, direction):
        self.neighbors[self.DIRS[direction]['name']] = neighbor
        neighbor.neighbors[self.DIRDATA[(self.DIRS[direction]['idx'] + 8) % 16]['name']] = self

    def get_neighbors(self):
        if not self.neighbors or time.time() - self.last_update > 3600:
            self.neighbors = self.server.get_neighbors(self)
        return self.neighbors


class LocationServer:
    INIT_LOC = 'Piątek'

    def __init__(self, url):
        # todo: zaimplementować LRU cache
        self.locations = {}
        self.url = url
        self.session = requests.session()
        res = self.call_camel(self.INIT_LOC, 'location')
        self.update_data(res['lau_code'])
        self.initial = res['lau_code']

    def authenticate(self, username, passwd):
        return self.session.post(f'{self.url}/auth', json={"user": username, "passwd": passwd}).json()

    def call_camel(self, name, what):
        while True:
            try:
                res = self.session.get(f'{self.url}/places/{name}/{what}')
                return res.json()
            except Exception as ex:
                print(f"Communication error: {ex}")
                print(f"Waiting 5 secs for retry")
                time.sleep(5)

    def get_neighbors(self, location):
        res = self.call_camel(location.loc_id, 'neighbors')
        return {
            Loc.DIRS[direction]['name']: self.locations.setdefault(
                neigh['lau_code'],
                Loc(self, neigh['lau_code'], neigh['name']))
            for direction, neigh in res.items()
            if direction in Loc.DIRS
        }

    def update_data(self, loc_id):
        loc = self.locations.get(loc_id)
        if not loc or not loc.coords:
            res = self.call_camel(loc_id, 'location')
            if not res:
                return
            if not loc:
                loc = Loc(self, res['lau_code'], res['name'], res['loc']['coordinates'],
                          res['county'], res['province'])
            else:
                loc.coords = res['loc']['coordinates']
                loc.county = res.get('county')
                loc.province = res.get('province')

        loc.neighbors = self.get_neighbors(loc)
        self.locations[loc_id] = loc


class Map:
    def __init__(self, url):
        self.url = url
        self.clients = {}
        self.client_idx = {}
        self.locserver = LocationServer(self.url)
        self.start_location = self.locserver.locations[self.locserver.initial]

        self.talker = Thread(target=self.handle_talk, daemon=True)
        self.talker.start()

    def authenticate(self, user, passwd):
        return self.locserver.authenticate(user, passwd)

    def add_client(self, client):
        if not hasattr(client, 'username'):
            client.username = ''
        if not hasattr(client, 'location'):
            client.location = self.start_location
        self.clients[id(client)] = {
            'start': time.time(),
            'last': time.time(),
            'client': client,
            'location': client.location
        }

    def location_change(self, client, new_location):
        self.locserver.update_data(new_location.loc_id)
        data = self.clients[id(client)]
        if data['location'].province != new_location.province:
            data['client'].writeresponse(f"You left province: {data['location'].province} and arrived to {new_location.province}")
        if data['location'].county != new_location.county:
            data['client'].writeresponse(f"You left county: {data['location'].county} and arrived to {new_location.county}")
        data['location'] = new_location

    def del_client(self, client):
        data = self.clients[id(client)]
        data['client'].writeresponse(f"\nFarewell - we've been together for {time.time() - data['start']} seconds")
        del self.clients[id(client)]

    def get_info(self, location, by_coords=False):
        if by_coords:
            srch_key = f'{location.coords[0]},{location.coords[1]},{location.name}'
        else:
            srch_key = location.name
        res = self.locserver.call_camel(srch_key, 'info')
        try:
            return res['query']['pages']
        except (KeyError, TypeError):
            return {}

    def handle_talk(self):
        while True:
            time.sleep(5)
            now = time.time()
            for client in self.clients.values():
                if now - client['last'] > 60:
                    client['client'].writeresponse(f"\nA minute passed again, total: {(now - client['start'])/60} mins")
                    client['last'] = now

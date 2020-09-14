#!/usr/bin/env python3

import logging
import socketserver
from telnetsrv.threaded import TelnetHandler, command
from location import Map, Loc

logging.getLogger('').setLevel(logging.DEBUG)


class MudServer(socketserver.TCPServer):
    allow_reuse_address = True


class MudHandler(TelnetHandler):
    WELCOME = "You have entered augmented text reality"
    authNeedUser = True
    authNeedPass = True
    world = None

    @classmethod
    def authCallback(cls, username, passwd):
        if True or username == 'scott' and passwd == 'tiger':
            self.location = self.world.start_location
            self.PROMPT = f'Real Geo MUD: {self.location["name"]}'
            return True
        raise Exception

    def __init__(self, request, client_address, server):
        self.PROMPT = 'Real Geo MUD> '
        super().__init__(request, client_address, server)

    def setup(self):
        self.world.add_client(self)
        super().setup()
        self.info()

    def finish(self):
        self.world.del_client(self)
        super().finish()

    @command('go')
    def go(self, params):
        where = Loc.DIRS[params[0].lower()]
        if where['name'] not in self.location.neighbors:
            self.writeresponse(f"You can't go {where['name']} from here")
        else:
            self.writeresponse(f"Going {where['name']}!")
            self.location = self.location.neighbors[where['name']]
            self.world.location_change(self)
        self.info()

    @command([di['short'] for di in Loc.DIRDATA])
    def go_to(self, params):
        self.go([self.input.cmd])

    @command('info')
    def info(self, params=None):
        neighs = ' '.join(data['short']
                          for data in Loc.DIRDATA
                          if data['name'] in self.location.neighbors)
        self.writeresponse(f'You are at {self.location.name}.')
        self.writeresponse(f'Available exits: {neighs}')


if __name__ == '__main__':
    MudHandler.world = Map('')
    server = MudServer(('', 10023), MudHandler)
    print("Starting server at port 10023")
    server.serve_forever()

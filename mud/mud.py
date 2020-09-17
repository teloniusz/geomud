#!/usr/bin/env python3

import logging
import re
import sys
import socketserver
from telnetsrv.threaded import TelnetHandler, command

from location import Map, Loc


logging.getLogger('').setLevel(logging.DEBUG)


class MudServer(socketserver.TCPServer):
    allow_reuse_address = True


class MudHandler(TelnetHandler):
    LDAP_BASE = 'dc=jnp2,dc=mimuw,dc=edu,dc=pl'
    LDAP_AUTHGROUP = f'cn=geomud,ou=authentication,ou=group,{LDAP_BASE}'
    LDAP_SERVER = 'authserver'

    WELCOME = "You have entered augmented text reality"
    authNeedUser = True
    authNeedPass = True
    world = None

    def authCallback(self, username, passwd):
        try:
            if not self.world.authenticate(username, passwd):
                self.writeresponse("Authentication failed")
                raise Exception('Access denied')
            self.username = username
            self.info()
            self.PROMPT = f'Real Geo MUD: {self.location.name}> '
        except Exception as ex:
            print(ex)
            raise
        return True

    def __init__(self, request, client_address, server):
        self.PROMPT = 'Real Geo MUD> '
        super().__init__(request, client_address, server)
        self.DOECHO = False

    def setup(self):
        self.world.add_client(self)
        super().setup()

    def finish(self):
        self.world.del_client(self)
        super().finish()

    @command('go')
    def go(self, params):
        """[<direction>]
        Go to direction
        """
        where = Loc.DIRS[params[0].lower()]
        if where['name'] not in self.location.neighbors:
            self.writeresponse(f"You can't go {where['name']} from here")
        else:
            self.writeresponse(f"Going {where['name']}!")
            new_location = self.location.neighbors[where['name']]
            self.world.location_change(self, new_location)
            self.location = new_location
            self.PROMPT = f'Real Geo MUD: {self.location.name}> '
        self.info()

    @command([di['short'] for di in Loc.DIRDATA])
    def go_to(self, params):
        """
        Go to direction
        """
        self.go([self.input.cmd])

    @command('loc')
    def info(self, params=None):
        """
        Show current location
        """
        neighs = ' '.join(data['short']
                          for data in Loc.DIRDATA
                          if data['name'] in self.location.neighbors)
        self.writeresponse(f'You are at {self.location.name}, county: {self.location.county}, province: {self.location.province}')
        self.writeresponse(f'Available exits: {neighs}')

    @command('info')
    def wiki(self, params):
        """
        Wiki info about current location
        """
        res = self.world.get_info(self.location)
        for page in res.values():
            self.writeresponse(f" * {page['title']}: {page['extract']}")

    @command('around')
    def around(self, params):
        """
        Wiki info about nearby pages
        """
        res = self.world.get_info(self.location, by_coords=True)
        for page in res.values():
            extract = page['extract'].replace("\n", "\n    ")
            self.writeresponse(f" * {page['title']}: {extract}")


if __name__ == '__main__':
    camel_server = 'camel'
    if len(sys.argv) > 1:
        camel_server = sys.argv[1]
    if not camel_server.startswith('http'):
        camel_server = 'http://' + camel_server
    MudHandler.world = Map(camel_server)
    server = MudServer(('', 10023), MudHandler)
    print("Starting server at port 10023")
    server.serve_forever()

import json
from backend import Backend
import sqlalchemy as sa


class LocBackend(Backend):
    DIRS = [
        ('s', -180, -168.75),
        ('ssw', -168.75, -146.25),
        ('sw', -146.25, -123.75),
        ('wsw', -123.75, -101.25),
        ('w', -101.25, -78.75),
        ('wnw', -78.75, -56.25),
        ('nw', -56.25, -33.75),
        ('nnw', -33.75, -11.25),
        ('n', -11.25, 11.25),
        ('nne', 11.25, 33.75),
        ('ne', 33.75, 56.25),
        ('ene', 56.25, 78.75),
        ('e', 78.75, 101.25),
        ('ese', 101.25, 123.75),
        ('se', 123.75, 146.25),
        ('sse', 146.25, 168.75),
        ('s', 168.75, 180)
    ]

    PROVS = {
        13423: 'zachodniopomorskie',
        13415: 'podkarpackie',
        13409: 'mazowieckie',
        13418: 'podlaskie',
        13422: 'warmińsko-mazurskie',
        13410: 'dolnośląskie',
        13413: 'łódzkie',
        13416: 'opolskie',
        13420: 'pomorskie',
        13412: 'małopolskie',
        13424: 'kujawsko-pomorskie',
        13414: 'lubuskie',
        13421: 'śląskie',
        13419: 'świętokrzyskie',
        13411: 'lubelskie',
        13417: 'wielkopolskie'
    }

    @classmethod
    def _get_dir(cls, azimuth):
        for name, start, end in cls.DIRS:
            if azimuth >= start and azimuth < end:
                return name

    def get_place(self, name=None, lau_code=None, county=False):
        def add_county(row):
            if county:
                row.update(self.get_county(row['loc']['coordinates']))
            return row

        args = {}
        if name:
            args['name'] = name
        if lau_code:
            args['lau_code'] = str(lau_code)
        query = self.db.execute(sa.text(
            'SELECT id, lau_code, name, ST_AsGeoJSON(ST_Centroid(location)) as loc FROM miejsca' +
            self.add_where(**args) +
            ' LIMIT 1'), **args)
        return (
            add_county(row)
            for row in self.results(query, dict(loc=json.loads)))

    def get_neighbors(self, name=None, lau_code=None):
        try:
            place = next(self.get_place(name, lau_code))
        except StopIteration:
            return None
        coords = '%f %f' % tuple(place['loc']['coordinates'])
        query = self.db.execute(
            f"""
SELECT p.lau_code, p.name, degrees(ST_Azimuth(ST_GeomFromText('POINT({coords})'), ST_Centroid(location))) as az, ST_Distance(ST_GeomFromText('POINT({coords})'), location) as dist
FROM miejsca p
ORDER BY p.location <-> ST_GeomFromText('POINT({coords})') LIMIT 16
            """)
        places = {}
        for row in self.results(query):
            if row['lau_code'] == place['lau_code']:
                continue
            direction = self._get_dir(row['az'])
            if direction not in places:
                places[direction] = row
        return places

    def get_county(self, coords):
        coords = '%f %f' % (coords[0], coords[1])
        query = self.db.execute(f"SELECT gid, jpt_kod_je, jpt_nazwa_, jpt_jor_id FROM powiaty WHERE ST_Contains(geom, ST_GeomFromText('POINT({coords})'))")
        res = list(self.results(query))
        if res:
            return {'county': res[0]['jpt_nazwa_'].replace('powiat ', ''),
                    'province': self.PROVS.get(res[0]['jpt_jor_id'])}
        return {'county': '', 'province': ''}

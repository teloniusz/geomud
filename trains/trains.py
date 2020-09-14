import re
import requests


class Trains:
    MAP_URL = 'https://portalpasazera.pl/MapaOL'
    MAP_REFRESH_URI = 'PociagiNaMapieAktualizacjaDanych'
    TOKEN_RE = 'input name="__RequestVerificationToken" type="hidden" value="([^"]+)"'
    HEADER_RE = '''[$][.]ajaxSetup[(][{] *headers: *[{] *'([^']+)': *'([^']+)' *[}] *[}]'''
    PROV_RE = '<option value="0">Wybierz województwo...</option>(.*)</select>'

    def __init__(self):
        self.session = requests.session()
        self.token = None
        self.headers = None
        self.provinces = None

    def load_data(self):
        res = self.session.get(self.MAP_URL)
        token_match = re.search(self.TOKEN_RE, res.text)
        if not token_match:
            raise ValueError(f"No validation token found on {self.MAP_URL}")
        self.token = token_match.group(1)
        prov_match = re.search(self.PROV_RE, res.text, flags=re.DOTALL)
        if not prov_match:
            raise ValueError(f"No province list found on {self.MAP_URL}")
        prov_opts = re.findall('<option value="(.*?)">(.*?)</option>', prov_match.group(1))
        self.provinces = {val.lower(): key for key, val in prov_opts}

        header_match = re.findall(self.HEADER_RE, res.text)
        self.headers = dict(header_match or {})
        self.headers.update({'__RequestVerificationToken': self.token})
        self.session.cookies['cookieAgreement'] = 'OK'

    def get_trains(self):
        if not self.token:
            self.load_data()
        res = self.session.post(f'{self.MAP_URL}/{self.MAP_REFRESH_URI}',
                                data={'jezyk': 'PL', '__RequestVerificationToken': self.token},
                                headers=self.headers)
        return res.json()['listaPociagow']['listaPociagow']


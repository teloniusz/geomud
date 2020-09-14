import requests


class Wiki:
    params = {'action': 'query', 'format': 'json'}

    def __init__(self, lang='pl'):
        self.endpoint = f'https://{lang}.wikipedia.org/w/api.php'
        self.session = requests.session()

    def _params(self, **kwargs):
        params = self.params.copy()
        params.update(dict(**kwargs))
        return params

    def get_coords(self, latitude, longitude, radius=1000, full=False):
        if full:
            get_params = self._params(
                prop='extracts|coordinates', exintro='', explaintext='', exsentences=3,
                generator='geosearch', ggscoord=f'{latitude}|{longitude}',
                ggslimit=20, ggsradius=radius)
        else:
            get_params = self._params(
                list='geosearch', gscoord=f'{latitude}|{longitude}',
                gslimit=20, gsradius=radius)
        return self.session.get(self.endpoint, params=get_params).json()

    def get_page(self, title, sentences=3):
        return self.session.get(self.endpoint, params=self._params(
            prop='extracts|coordinates', exintro='', explaintext='', exsentences=sentences,
            titles=title)).json()


def show(res):
    if 'error' in res:
        print(f"Error: {res['error']['code']}: {res['error']['info']}")
        return
    data = res['query']
    if 'pages' in data:
        data = data['pages']
    for key, results in data.items() if type(data) == dict else enumerate(data):
        print(f'{key}:')
        for rec in results if type(results) == list else results.items():
            print(f'   {rec}')

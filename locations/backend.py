from sqlalchemy import create_engine


class Backend:
    connect_string = None
    _instance = None
    engine = None

    # singleton pattern
    @classmethod
    def instance(cls):
        if not cls._instance:
            if not cls.connect_string:
                raise ValueError('Provide connect string before getting an instance')
            cls.engine = create_engine(cls.connect_string)
            cls._instance = cls()
        return cls._instance

    @staticmethod
    def results(query, mapping=None):
        if mapping is None:
            mapping = {}
        for row in query.cursor:
            res = {}
            for idx, name in enumerate(query.keys()):
                transform = mapping.get(name, mapping.get(idx))
                res[name] = transform(row[idx]) if callable(transform) else row[idx]
            yield res

    @staticmethod
    def add_where(**kwargs):
        if not kwargs:
            return
        return ' WHERE ' + ' AND '.join(f'{key} = :{key}' for key in kwargs)

    def __init__(self):
        self.db = self.engine.connect()

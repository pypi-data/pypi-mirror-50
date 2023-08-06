from pony.orm import Database, Required, PrimaryKey, Json, db_session, select, commit, desc
from datetime import datetime
from copy import copy


class StoreMeta:
    def __init__(self, elem):
        self.id = id
        self.key = elem.key
        self.value = elem.value
        self.create = elem.create.strftime("%Y-%m-%dT%H:%M:%S")
        self.update = elem.update.strftime("%Y-%m-%dT%H:%M:%S")


class Store(object):
    def __init__(self,
                 driver='postgres', user='root', password='dangerous',
                 host='localhost', database='test', port=5432):

        self.tablename = self.__class__.__name__
        if driver not in ['mysql', 'postgres']:
            raise Exception('not implemented!')
        self.database = Database(
            driver, user=user, password=password, host=host, database=database, port=port)

        schema = dict(
            id=PrimaryKey(int, auto=True),
            create=Required(datetime, sql_default='CURRENT_TIMESTAMP',
                            default=lambda: datetime.utcnow()),
            update=Required(datetime, sql_default='CURRENT_TIMESTAMP',
                            default=lambda: datetime.utcnow()),
            key=Required(str, index=True, unique=True),
            value=Required(Json, volatile=True)
        )

        self.store = type(self.tablename, (self.database.Entity,), schema)
        self.database.generate_mapping(create_tables=True, check_tables=True)

    @db_session
    def __setattr__(self, key, value):
        if key in ['store', 'database', 'tablename', '__class__']:
            return super().__setattr__(key, value)
        item = select(e for e in self.store if e.key == key).order_by(
            lambda o: desc(o.create)).first()
        if item is None:
            self.store(key=key, value=value)
        else:
            item.value = value
            item.update_at = datetime.utcnow()

    @db_session
    def __getattribute__(self, key):
        if key in ['store', 'database', 'tablename', '__class__'] or key.startswith('_'):
            return object.__getattribute__(self, key)

        elem = select(e for e in self.store if e.key == key).order_by(
            lambda o: desc(o.create)).first()
        if elem:
            return StoreMeta(elem)
        return None

    @db_session
    def __setitem__(self, key, value):
        if isinstance(key, slice):
            raise Exception('not implemented!')
        elif isinstance(key, tuple):
            if len(key) == 2:
                elems = self._getitem_query_tuple(key)
                if elems:
                    now = datetime.utcnow()
                    for elem in elems:
                        elem.value = value
                        elem.update_at = now
                    return
            raise Exception('not implemented!')
        elif isinstance(key, str):

            if '=' in key or ':' in key:
                updated_key = ['*', key]
                elems = self._getitem_query_tuple(updated_key)
                if elems:
                    now = datetime.utcnow()
                    for elem in elems:
                        elem.value = value
                        elem.update_at = now
                return

            item = select(e for e in self.store if e.key == key).order_by(lambda o: desc(o.create)).first()
            if item is None:
                self.store(key=key, value=value)
            else:
                item.value = value
                item.update_at = datetime.utcnow()

    @db_session
    def __getitem__(self, key):
        if isinstance(key, slice):
            raise Exception('not implemented!')
        elif isinstance(key, tuple):
            if len(key) == 2:
                elems = self._getitem_query_tuple(key)
                return [StoreMeta(elem) for elem in elems]
            raise Exception('not implemented!')
        elif isinstance(key, str):
            if '=' in key or ':' in key:
                updated_key = ['*', key]
                elems = self._getitem_query_tuple(updated_key)
                return [StoreMeta(elem) for elem in elems]
            elem = select(e for e in self.store if e.key == key).order_by(
                lambda o: desc(o.create)).first()
            if elem:
                return StoreMeta(elem)
        return []

    @db_session
    def _getitem_query_tuple(self, key):
        if key[0] == '*':
            if '=' in key[1]:
                k, v = key[1].split('=', 1)
                elems = select(e for e in self.store if e.value[k] == v).order_by(lambda o: desc(o.create))[:]
            elif ':' in key[1]:
                k, v = key[1].split(':', 1)
                elems = select(e for e in self.store if e.value[k] == v).order_by(lambda o: desc(o.create))[:]
            else:
                elems = select(e for e in self.store if e.value[key[1]]).order_by(lambda o: desc(o.create))[:]
        else:
            if '=' in key[1]:
                k, v = key[1].split('=', 1)
                elems = select(e for e in self.store if e.key == key[0] and e.value[key[1]]).order_by(lambda o: desc(o.create))[:]
            elif ':' in key[1]:
                k, v = key[1].split(':', 1)
                elems = select(e for e in self.store if e.key == key[0] and e.value[key[1]]).order_by(lambda o: desc(o.create))[:]
            else:
                elems = select(e for e in self.store if e.key == key[0] and e.value[key[1]]).order_by(lambda o: desc(o.create))[:]
        return elems


class Tiger(Store):
    pass


if __name__ == "__main__":
    # s = Tiger(user='dameng', password='pythonic', database='mytest')
    s = Tiger(driver='mysql', user='root', password='dangerous123',
              database='mytest', port=8306, host='127.0.0.1')
    s['m'] = {'2': '3'}
    print([{e.key: e.value} for e in s['*', '2=3']])
    s['*', '2=3'] = {'m': 'n'}
    print([{e.key: e.value} for e in s['m=n']])

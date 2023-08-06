from pony.orm import Database, Required, PrimaryKey, Json, db_session, select, commit, desc
from datetime import datetime
from copy import copy
import uuid
import json

class StoreMetas:
    def __init__(self, elems, store=None):
        self.elems = [StoreMeta(elem, store=store) for elem in elems]

    def __str__(self):
        return '\n'.join([str(elem) for elem in self.elems])
            
    @db_session
    def __getitem__(self, key):
        if isinstance(key, int):
            return self.elems[key]

        return [elem[key] for elem in self.elems]

    @db_session
    def __setitem__(self, key, value):
        if isinstance(key, int):
            self.elems[key] = value
            return
        for elem in self.elems:
            elem[key] = value



class StoreMeta:
    def __init__(self, elem, store=None):
        self.store = store
        self.id = elem.id
        self.key = elem.key
        self.value = elem.value
        self.create = elem.create.strftime("%Y-%m-%dT%H:%M:%S")
        self.update = elem.update.strftime("%Y-%m-%dT%H:%M:%S")

    def __str__(self):
        return "id: {}, key: {}, value: {}, create: {}, update: {}".format(self.id, self.key, self.value,
                                                                           self.create, self.update)

    @db_session
    def __assign__(self, value):
        elem = select(e for e in self.store if e.id == self.id).order_by(lambda o: desc(o.create)).first()
        if elem is None:
            raise Exception('elem not found')
        else:
            elem.value = value
            elem.update_at = datetime.utcnow()
            self.value = elem.value
            self.update = elem.update.strftime("%Y-%m-%dT%H:%M:%S")

    @db_session
    def __setattr__(self, key, value):
        if key in ['store','id', 'key', 'value', 'create', 'update'] or key.startswith('_'):
            return super().__setattr__(key, value)
        elem = select(e for e in self.store if e.id == self.id).order_by(lambda o: desc(o.create)).first()
        if elem is None:
            raise Exception('elem not found')
        else:
            if isinstance(elem.value, dict):
                elem.value[key] = value
                elem.update_at = datetime.utcnow()
                self.value = elem.value
                self.update = elem.update.strftime("%Y-%m-%dT%H:%M:%S")
            else:
                raise Exception('value not dict!')

    @db_session
    def __getattribute__(self, key):
        if key in ['store','id', 'key', 'value', 'create', 'update'] or key.startswith('_'):
            return object.__getattribute__(self, key)

        elem = select(e for e in self.store if e.id == self.id).order_by(lambda o: desc(o.create)).first()
        if elem:
            if isinstance(elem.value, dict):
                return elem.value.get(key)

    @db_session
    def __setitem__(self, key, value):
        elem = select(e for e in self.store if e.id == self.id).order_by(lambda o: desc(o.create)).first()
        if elem is None:
            raise Exception('elem not found')
        else:
            if isinstance(elem.value, dict) or \
               (isinstance(key, int) and isinstance(elem.value, list)):
                elem.value[key] = value
                elem.update_at = datetime.utcnow()
                self.value = elem.value
                self.update = elem.update.strftime("%Y-%m-%dT%H:%M:%S")
            else:
                raise Exception('value not dict!')

    @db_session
    def __getitem__(self, key):
        elem = select(e for e in self.store if e.id == self.id).order_by(lambda o: desc(o.create)).first()
        if elem:
            if isinstance(elem.value, dict)or \
               (isinstance(key, int) and isinstance(elem.value, list)) or \
               (isinstance(key, int) and isinstance(elem.value, str)) :
                return elem.value[key]

class Store(object):
    def __init__(self,
                 driver='postgres', user='root', password='dangerous',
                 host='localhost', database='test', port=5432,
                 begin=None, end=None):

        self.begin = begin
        self.end = end
        self.tablename = self.__class__.__name__
        if driver not in ['mysql', 'postgres']:
            raise Exception('not implemented!')
        self.database = Database(
            driver, user=user, password=password, host=host, database=database, port=port)

        schema = dict(
            id=PrimaryKey(int, auto=True),
            create=Required(datetime, sql_default='CURRENT_TIMESTAMP', default=lambda: datetime.utcnow()),
            update=Required(datetime, sql_default='CURRENT_TIMESTAMP', default=lambda: datetime.utcnow()),
            key=Required(str, index=True, unique=True),
            value=Required(Json, volatile=True)
        )

        self.store = type(self.tablename, (self.database.Entity,), schema)
        self.database.generate_mapping(create_tables=True, check_tables=True)

    @db_session
    def __setattr__(self, key, value):
        if key in ['store', 'database', 'tablename', 'begin', 'end', 'add'] or key.startswith('_'):
            return super().__setattr__(key, value)
        item = select(e for e in self.store if e.key == key).order_by(lambda o: desc(o.create)).first()
        if item is None:
            self.store(key=key, value=value)
        else:
            item.value = value
            item.update_at = datetime.utcnow()

    @db_session
    def __getattribute__(self, key):
        if key in ['store', 'database', 'tablename', 'begin', 'end', 'add'] or key.startswith('_'):
            return object.__getattribute__(self, key)

        elem = select(e for e in self.store if e.key == key).order_by(lambda o: desc(o.create)).first()
        if elem:
            return StoreMeta(elem, store=self.store)
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
                return StoreMetas(elems, store=self.store)#[StoreMeta(elem) for elem in elems]
            raise Exception('not implemented!')
        elif isinstance(key, str):
            if '=' in key or ':' in key:
                updated_key = ['*', key]
                elems = self._getitem_query_tuple(updated_key)
                return StoreMetas(elems, store=self.store)#[StoreMeta(elem) for elem in elems]
            elem = select(e for e in self.store if e.key == key).order_by(
                lambda o: desc(o.create)).first()
            if elem:
                return StoreMeta(elem, store=self.store)
        return []

    @db_session
    def _getitem_query_tuple(self, key):
        if key[0] == '*':
            if '=' in key[1]:
                k, v = key[1].split('=', 1)
                elems = select(e for e in self.store if e.value[k] == v).order_by(lambda o: desc(o.create))
            elif ':' in key[1]:
                k, v = key[1].split(':', 1)
                elems = select(e for e in self.store if e.value[k] == v).order_by(lambda o: desc(o.create))
            else:
                elems = select(e for e in self.store if e.value[key[1]]).order_by(lambda o: desc(o.create))
        else:
            if '=' in key[1]:
                k, v = key[1].split('=', 1)
                elems = select(e for e in self.store if e.key == key[0] and e.value[key[1]]).order_by(lambda o: desc(o.create))
            elif ':' in key[1]:
                k, v = key[1].split(':', 1)
                elems = select(e for e in self.store if e.key == key[0] and e.value[key[1]]).order_by(lambda o: desc(o.create))
            else:
                elems = select(e for e in self.store if e.key == key[0] and e.value[key[1]]).order_by(lambda o: desc(o.create))
        if self.begin and self.end:
            elems = elems[self.begin:self.end]
        elif self.begin:
            elems = elems[self.begin:]
        elif self.end:
            elems = elems[:self.end]
        else:
            elems = elems[:]

        return elems

    @db_session
    def add(self, value):
        hex = uuid.uuid1().hex
        self.store(key="store_{}".format(hex), value=value)




class Tiger(Store):
    pass

if __name__ == "__main__":
    s = Tiger(driver='mysql', user='root', password='dangerous123',
              database='mytest', port=8306, host='127.0.0.1')

    s['t1'] = "hello"
    print(s['t1'].key, s['t1'].value)
    # # tiger
    # # key   value
    # # t1    hello
    s['t2'] = ["hello", "world"]
    print(s['t2'].key, s['t2'].value)
    # # key   value
    # # t1    hello
    # # t2    ["hello", "world"]
    s['t3'] = {'hello': 'world'}
    print(s['t3'].key, s['t3'].value)
    # # key   value
    # # t1    hello
    # # t2    ["hello", "world"]
    # # t3    {'hello': 'world'}
    s['t4'] = {'hello': 'python'}
    print(s['t4'].key, s['t4'].value)
    # # key   value
    # # t1    hello
    # # t2    ["hello", "world"]
    # # t3    {'hello': 'world'}
    # # t4    {'hello': 'python'}
    print([e.key for e in s['*', 'hello']])
    # # 匹配到key为任意值， value中存在key为hello的 数据
    # # ['t3', 't4']
    # print([e.key for e in s['*', 'hello=python']])
    # # 匹配到key为任意值， value中存在hello=python的 数据
    # # ['t4'] 



    print(s.t4.hello)

    print('..............................')

    s.m1 = [1, 2]
    print(s.m1[0])
    print(s.m1[1])
    print(s.m1)



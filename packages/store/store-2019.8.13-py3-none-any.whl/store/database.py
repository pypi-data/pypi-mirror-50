from pony.orm import Database, Required, PrimaryKey, Json, db_session, select, commit, desc, delete, count
from datetime import datetime
from copy import copy
import os
import uuid
import json


class StoreMetas:
    def __init__(self, elems, store=None):
        self.elems = [StoreMeta(elem, store=store) for elem in elems]

    def __str__(self):
        return '\n'.join([str(elem) for elem in self.elems])

    def __len__(self):
        return len(self.elems)

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

    @db_session
    def __getattribute__(self, key):
        if key in ['elems'] or key.startswith('_'):
            return object.__getattribute__(self, key)

        if key in ['store', 'id', 'key', 'value', 'create', 'update']:
            return [elem.key for elem in self.elems]
        return [elem[key] for elem in self.elems]


class StoreMeta:
    def __init__(self, elem, store=None):
        self.store = store
        self.id = elem.id
        self.key = elem.key
        self.value = elem.value
        self.create = elem.create.strftime("%Y-%m-%dT%H:%M:%S")
        self.update = elem.update.strftime("%Y-%m-%dT%H:%M:%S")

    def __str__(self):
        return "id: {}, key: {}, value: {}, create: {}, update: {}".format(self.id, self.key, self.value, self.create, self.update)

    @db_session
    def __assign__(self, value):
        elem = select(e for e in self.store if e.id == self.id).order_by(lambda o: desc(o.create)).order_by(lambda o: desc(o.id)).first()
        if elem is None:
            raise Exception('elem not found')
        else:
            elem.value = value
            elem.update = datetime.utcnow()

            self.value = elem.value
            self.update = elem.update.strftime("%Y-%m-%dT%H:%M:%S")

    @db_session
    def __setattr__(self, key, value):
        if key in ['store', 'id', 'key', 'value', 'create', 'update'] or key.startswith('_'):
            return super().__setattr__(key, value)
        elem = select(e for e in self.store if e.id == self.id).order_by(lambda o: desc(o.create)).order_by(lambda o: desc(o.id)).first()
        if elem is None:
            raise Exception('elem not found')
        else:
            if isinstance(elem.value, dict):
                elem.value[key] = value
                elem.update = datetime.utcnow()

                self.value = elem.value
                self.update = elem.update.strftime("%Y-%m-%dT%H:%M:%S")
            else:
                raise Exception('value not dict!')

    @db_session
    def __getattribute__(self, key):
        if key in ['store', 'id', 'key', 'value', 'create', 'update'] or key.startswith('_'):
            return object.__getattribute__(self, key)

        elem = select(e for e in self.store if e.id == self.id).order_by(lambda o: desc(o.create)).order_by(lambda o: desc(o.id)).first()
        if elem:
            if isinstance(elem.value, dict):
                return elem.value.get(key)

    @db_session
    def __setitem__(self, key, value):
        elem = select(e for e in self.store if e.id == self.id).order_by(lambda o: desc(o.create)).order_by(lambda o: desc(o.id)).first()
        if elem is None:
            raise Exception('elem not found')
        else:
            if isinstance(elem.value, dict) or \
               (isinstance(key, int) and isinstance(elem.value, list)):
                elem.value[key] = value
                elem.update = datetime.utcnow()

                self.value = elem.value
                self.update = elem.update.strftime("%Y-%m-%dT%H:%M:%S")
            else:
                raise Exception('value not dict!')

    @db_session
    def __getitem__(self, key):
        elem = select(e for e in self.store if e.id == self.id).order_by(lambda o: desc(o.create)).order_by(lambda o: desc(o.id)).first()
        if elem:
            if isinstance(elem.value, dict) or \
               (isinstance(key, int) and isinstance(elem.value, list)) or \
               (isinstance(key, int) and isinstance(elem.value, str)):
                if isinstance(key, int):
                    return elem.value[key]
                else:
                    return elem.value.get(key)
            



class Store(object):
    _safe_attrs = ['store', 'database', 'tablename', 'begin',
                   'end', 'add', 'register_attr', 'slice', 'adjust_slice', 'provider',
                   'query_key', 'query_value']

    def __init__(self,
                 provider=None, user=None, password=None,
                 host=None, port=None, database=None, filename=None,
                 begin=None, end=None):

        if provider == 'postgres':
            self.database = Database(provider, user=user or 'postgres', password=password or 'postgres',
                                     host=host or 'localhost', port=port or 5432, database=database or 'postgres')
        elif provider == 'mysql':
            self.database = Database(provider, user=user or 'root', password=password or 'dangerous',
                                     host=host or 'localhost', port=port or 3306, database=database or 'mysql')
        elif provider == 'sqlite':
            if not filename:
                filename = 'database.sqlite'
            if not filename.startswith('/'):
                filename = os.getcwd()+'/' + filename
            self.database = Database(
                provider, filename=filename, create_db=True)
        else:
            raise Exception('not implemented!')

        self.provider = provider

        self.begin, self.end = begin, end
        self.tablename = self.__class__.__name__

        schema = dict(
            id=PrimaryKey(int, auto=True),
            create=Required(datetime, sql_default='CURRENT_TIMESTAMP', default=lambda: datetime.utcnow()),
            update=Required(datetime, sql_default='CURRENT_TIMESTAMP', default=lambda: datetime.utcnow()),
            key=Required(str, index=True, unique=True),
            value=Required(Json, volatile=True)
        )

        self.store = type(self.tablename, (self.database.Entity,), schema)
        self.database.generate_mapping(create_tables=True, check_tables=True)

    def slice(self, begin, end):
        self.begin, self.end = begin, end

    @staticmethod
    def register_attr(name):
        if isinstance(name, str) and name not in Store._safe_attrs:
            Store._safe_attrs.append(name)

    @db_session
    def __setattr__(self, key, value):
        if key in Store._safe_attrs or key.startswith('_'):
            return super().__setattr__(key, value)
        item = select(e for e in self.store if e.key == key).order_by(lambda o: desc(o.create)).order_by(lambda o: desc(o.id)).first()
        if item is None:
            self.store(key=key, value=value)
        else:
            item.value = value
            item.update = datetime.utcnow()

    @db_session
    def __getattribute__(self, key):
        if key in Store._safe_attrs or key.startswith('_'):
            return object.__getattribute__(self, key)

        elem = select(e for e in self.store if e.key == key).order_by(lambda o: desc(o.create)).order_by(lambda o: desc(o.id)).first()
        if elem:
            return StoreMeta(elem, store=self.store)
        return None

    @db_session
    def __setitem__(self, key, value):

        if isinstance(key, slice):
            raise Exception('not implemented!')
        elif isinstance(key, tuple):
            if len(key) > 4:
                raise Exception('not implemented!')
            elems = self._query_value(*key)
            if elems:
                now = datetime.utcnow()
                for elem in elems:
                    elem.value = value
                    elem.update = now
            else:
                raise Exception('not implemented')
            return
        elif isinstance(key, str):
            
            if ',' in key:
                keys = key.split(',')
                elems = self._query_value(*keys)
                if elems:
                    now = datetime.utcnow()
                    for elem in elems:
                        elem.value = value
                        elem.update = now
                else:
                    raise Exception('not implemented')
                return

            elif '=' in key or '>' in key or '<' in key or ':' in key:
                elems = self.query_value(key)
                if elems:
                    now = datetime.utcnow()
                    for elem in elems:
                        elem.value = value
                        elem.update = now
                else:
                    raise Exception('not implemented')
                return

            elif key == '*':
                elems = select(e for e in self.store).order_by(lambda o: desc(o.create)).order_by(lambda o: desc(o.id))
                elems = self.adjust_slice(elems)

                if elems:
                    now = datetime.utcnow()
                    for elem in elems:
                        elem.value = value
                        elem.update = now
                else:
                    self.store(key=key, value=value)
                return


            elem = select(e for e in self.store if e.key == key).order_by(lambda o: desc(o.create)).order_by(lambda o: desc(o.id)).first()
            if elem:
                elem.value = value
                elem.update = datetime.utcnow()
            else:
                self.store(key=key, value=value)
            return
        raise Exception('not implemented!')

    @db_session
    def __getitem__(self, key):
        if isinstance(key, slice):
            raise Exception('not implemented!')
        elif isinstance(key, tuple):
            if len(key) > 4:
                raise Exception('not implemented!')
            return self.query_value(*key)
        elif isinstance(key, str):
            if ',' in key:
                keys = key.split(',')
                return self.query_value(*keys)

            if '=' in key or '>' in key or '<' in key or ':' in key:
                return self.query_value(key)

            if key == '*':
                elems = select(e for e in self.store).order_by(lambda o: desc(o.create)).order_by(lambda o: desc(o.id))
                elems = self.adjust_slice(elems)
                return StoreMetas(elems, store=self.store)

            elem = select(e for e in self.store if e.key == key).order_by(lambda o: desc(o.create)).order_by(lambda o: desc(o.id)).first()
            if elem:
                return StoreMeta(elem, store=self.store)
        return []

    @db_session
    def __delitem__(self, key):
        if isinstance(key, slice):
            raise Exception('not implemented!')
        elif isinstance(key, tuple):
            if len(key) > 4:
                raise Exception('not implemented!')
            elems = self._query_value(*key)
            if elems:
                for elem in elems:
                    elem.delete()
            return
        elif isinstance(key, str):
            
            if ',' in key:
                keys = key.split(',')
                elems = self._query_value(*keys)
                if elems:
                    for elem in elems:
                        elem.delete()
                return

            elif '=' in key or '>' in key or '<' in key or ':' in key:
                elems = self._query_value(key)
                if elems:
                    for elem in elems:
                        elem.delete()
                return

            elif key == '*':
                elems = select(e for e in self.store).order_by(lambda o: desc(o.create)).order_by(lambda o: desc(o.id))
                elems = self.adjust_slice(elems)

                if elems:
                    for elem in elems:
                        elem.delete()
                return


            elem = select(e for e in self.store if e.key == key).order_by(lambda o: desc(o.create)).order_by(lambda o: desc(o.id)).first()
            if elem:
                elem.delete()
                return 
        raise Exception('not implemented!')

    @db_session
    def __delattr__(self, key):
        delete(e for e in self.store if e.key == key)


    @db_session
    def add(self, value):
        hex = uuid.uuid1().hex
        key = "store_{}".format(hex)
        self.store(key=key, value=value)
        return key

    @db_session
    def _query_key(self, key):
        return select(e for e in self.store if e.id == self.id).order_by(lambda o: desc(o.create)).order_by(lambda o: desc(o.id)).first()

    @db_session
    def query_key(self, key):
        elem = self._query_key(key)
        if elem:
            return StoreMeta(elem, store=self.store)

    # ugly implementation
    @db_session
    def _query_value(self, *keys):
        try:
            lenkeys = len(keys)
            if lenkeys == 1:
                if self.provider == 'mysql':
                    if '>=' in keys[0]:
                        key, value = keys[0].split('>=', 1)
                        elems = select(e for e in self.store if e.value[key] >= float(value))
                    elif '<=' in keys[0]:
                        key, value = keys[0].split('<=', 1)
                        elems = select(e for e in self.store if e.value[key] <= float(value))
                    elif '=' in keys[0]:
                        key, value = keys[0].split('=', 1)
                        elems = select(e for e in self.store if e.value[key] == value)
                    elif '>' in keys[0]:
                        key, value = keys[0].split('>', 1)
                        elems = select(e for e in self.store if e.value[key] > float(value))
                    elif '<' in keys[0]:
                        key, value = keys[0].split('<', 1)
                        elems = select(e for e in self.store if e.value[key] < float(value))
                    elif ':' in keys[0]:
                        key, value = keys[0].split(':', 1)
                        elems = select(e for e in self.store if value in e.value[key])
                    else:
                        elems = select(e for e in self.store if e.value[keys[0]] != None)
                else:
                    if '>=' in keys[0]:
                        key, value = keys[0].split('>=', 1)
                        elems = select(e for e in self.store if e.value[key] >= float(value))
                    elif '<=' in keys[0]:
                        key, value = keys[0].split('<=', 1)
                        elems = select(e for e in self.store if e.value[key] <= float(value))
                    elif '=' in keys[0]:
                        key, value = keys[0].split('=', 1)
                        elems = select(e for e in self.store if e.value[key] == value)
                    elif '>' in keys[0]:
                        key, value = keys[0].split('>', 1)
                        elems = select(e for e in self.store if e.value[key] > float(value))
                    elif '<' in keys[0]:
                        key, value = keys[0].split('<', 1)
                        elems = select(e for e in self.store if e.value[key] < float(value))
                    elif ':' in keys[0]:
                        key, value = keys[0].split(':', 1)
                        elems = select(e for e in self.store if value in e.value[key])
                    else:
                        elems = select(e for e in self.store if keys[0] in e.value )
            elif lenkeys == 2:
                if '>=' in keys[1]:
                    key, value = keys[1].split('>=', 1)
                    elems = select(e for e in self.store if e.value[keys[0]][key] >= float(value))
                elif '<=' in keys[1]:
                    key, value = keys[1].split('<=', 1)
                    elems = select(e for e in self.store if e.value[keys[0]][key] <= float(value))
                elif '=' in keys[1]:
                    key, value = keys[1].split('=', 1)
                    elems = select(e for e in self.store if e.value[keys[0]][key] == value)
                elif '>' in keys[1]:
                    key, value = keys[1].split('>', 1)
                    elems = select(e for e in self.store if e.value[keys[0]][key] > float(value))
                elif '<' in keys[1]:
                    key, value = keys[1].split('<', 1)
                    elems = select(e for e in self.store if e.value[keys[0]][key] < float(value))
                elif ':' in keys[1]:
                    key, value = keys[1].split(':', 1)
                    elems = select(e for e in self.store if value in e.value[keys[0]][key])
                else:
                    elems = select(e for e in self.store if keys[1] in e.value[keys[0]])
            elif lenkeys == 3:
                if '>=' in keys[2]:
                    key, value = keys[2].split('>=', 1)
                    elems = select(e for e in self.store if  e.value[keys[0]][keys[1]][key] >= value)
                elif '<=' in keys[2]:
                    key, value = keys[2].split('<=', 1)
                    elems = select(e for e in self.store if  e.value[keys[0]][keys[1]][key] <= value)
                elif '=' in keys[2]:
                    key, value = keys[2].split('=', 1)
                    elems = select(e for e in self.store if  e.value[keys[0]][keys[1]][key] == value)
                elif '>' in keys[2]:
                    key, value = keys[2].split('>', 1)
                    elems = select(e for e in self.store if  e.value[keys[0]][keys[1]][key] > value)
                elif '<' in keys[2]:
                    key, value = keys[2].split('<', 1)
                    elems = select(e for e in self.store if  e.value[keys[0]][keys[1]][key] < value)
                elif ':' in keys[2]:
                    key, value = keys[2].split(':', 1)
                    elems = select(e for e in self.store if  value in e.value[keys[0]][keys[1]][key])
                else:
                    elems = select(e for e in self.store if keys[2] in e.value[keys[0]][keys[1]])
            elif lenkeys == 4:
                if '>=' in keys[3]:
                    key, value = keys[3].split('>=', 1)
                    elems = select(e for e in self.store if e.value[keys[0]][keys[1]][keys[2]][key] >= value)
                elif '<=' in keys[3]:
                    key, value = keys[3].split('<=', 1)
                    elems = select(e for e in self.store if e.value[keys[0]][keys[1]][keys[2]][key] <= value)
                elif '=' in keys[3]:
                    key, value = keys[3].split('=', 1)
                    elems = select(e for e in self.store if e.value[keys[0]][keys[1]][keys[2]][key] == value)
                elif '>' in keys[3]:
                    key, value = keys[3].split('>', 1)
                    elems = select(e for e in self.store if e.value[keys[0]][keys[1]][keys[2]][key] > value)
                elif '<' in keys[3]:
                    key, value = keys[3].split('<', 1)
                    elems = select(e for e in self.store if e.value[keys[0]][keys[1]][keys[2]][key] < value)
                elif ':' in keys[3]:
                    key, value = keys[3].split(':', 1)
                    elems = select(e for e in self.store if value in e.value[keys[0]][keys[1]][keys[2]][key])
                else:
                    elems = select(e for e in self.store if keys[3] in e.value[keys[0]][keys[1]][keys[2]])
            else:
                raise Exception('not implemented!')

            if elems:
                elems = self.adjust_slice(elems)
                if elems:
                    return elems
        except TypeError:
            raise Exception('key invalid!')
        return []

    @db_session
    def query_value(self, *keys):
        elems = self._query_value(*keys)
        return StoreMetas(elems, store=self.store)

    def adjust_slice(self, elems):
        begin, end = self.begin, self.end
        if begin and end:
            if begin < 0:
                begin = len(self) + begin
            if end < 0:
                end = len(self) + end
            if begin > end:
                begin, end = end, end
            elems = elems[begin:end]
        elif begin:
            if begin < 0:
                begin = len(self) + begin
            elems = elems[begin:]
        elif end:
            if end < 0:
                end = len(self) + end
            elems = elems[:end]
        else:
            elems = elems[:]
        return elems

    @db_session
    def __len__(self):
        return count(e for e in self.store)


class Tiger(Store):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Store.register_attr('test')

    def test(self):
        print('test')


def test(t):
    t.a = {
        'name': 'king'
    }
    print(t['name=king'].name)


if __name__ == "__main__":
    import time
    # t = Tiger(provider='postgres', user='dameng', password='pythonic',
    #           database='mytest', port=5432, host='127.0.0.1')
    t = Tiger(provider='mysql', user='root', password='dangerous123',
              database='mytest', port=8306, host='127.0.0.1')
    # t = Tiger('sqlite')
    # t.slice(0,10)
    # print(t['*'])
    # print('.....')

    # t.slice(10,15)
    # print(t['*']['like'])
    # t.test()
    # t.add({'hello': 1})
    # t.add({'hello': 2})
    # print(t['*'])
    # print(t.sum(lambda e: e.value['hello'] == 'world', 'hello') )
    # print(sum[t['hello=1']['hello']])
    # print(len(t))
    # print(sum(t['hello=1']['hello']))

    # import time
    # time.sleep(60)
    t.a = {"a1": {"b1": {"c1": {"d1": 14, "d2": ["123", "ab"]}, "c2":30}}, "a2": {"b2": [], "b22": {"c22": 123}}, "a3": []}
    # print(t.query_keys("a3"))
    # print(t.query_keys("a1", "b1"))
    # print(t.query_keys("a2", "b2"))
    # print(t['*', "a3"])
    print(t.query_value("a1", "b1", "c1", "d1=14"))
    print(t["a1", "b1", "c1", "d1=14"])
    print(t["a1,b1,c1,d1=14"])
    print(t["a1,b1,c1,d1=14"]['a1'])
    # time.sleep(1)
    for e in t["a1,b1,c1,d1=14"]:
        print(e['a1']['b1']['c1'])
        e['m1'] = 10
    # time.sleep(1)
    for e in t["a1,b1,c1,d1=14"]:
        print(e)
    t["a1,b1,c1,d1=14"]['m1'] = 20
    # time.sleep(1)
    for e in t["a1,b1,c1,d1=14"]:
        print(e)
    # print(t["a1,b1,c1,d1=14"]['a1']['b1'])
    # t["a1,b1,c1,d1=14"]['a1'] = 15
    # print(t.a)
    # print(t.query_value("a1", "b1", "c2=10"))
    t.a = {"a1": {"b1": {"c1": {"d1": 14, "d2": ["123", "ab"]}, "c2":30}}, "a2": {"b2": [], "b22": {"c22": 123}}, "m2": [{"n1": "hello"}, {"n2": "world"}]}
    print(type(t['m2','n2']))
    print(type(t['a1','b1']))




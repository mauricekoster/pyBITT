"""A key/value store for configuration items

Example:
>>> from MemoryStore import MemoryStore
>>> store = MemoryStore()
>>> conf = Configuration(store)
>>> conf.set_item('test', 'hello world!')
>>> conf.set_item('other', 'bye bye!')
>>> conf['message'] = 'This is a test'
>>> print(conf.get())
{'test': 'hello world!', 'message': 'This is a test', 'other': 'bye bye!'}
>>> print conf['test']
hello world!
"""

class Configuration:
    def __init__(self, store):
        self.store = store
        self.table_name = 'configuration'
        self.table_def = {
            'name': self.table_name,
            "fields": [

                {'name': 'key', 'type': 'char', 'length': 20},
                {'name': 'value', 'type': 'char', 'length': 1000}
            ],
            'primary_key': 'key'
        }
        self.store.register_table(self.table_def)

    def get_item(self, key):
        result = self.store.get_records(self.table_name, key=key)
        if result:
            return result[0]['value']
        return None

    def __getitem__(self, item):
        return self.get_item(item)

    def set_item(self, key, value):
        self.store.store_record(self.table_name, {'key': key, 'value': value})

    def __setitem__(self, key, value):
        self.set_item(key, value)

    def get(self):
        results = self.store.get_records(self.table_name)
        d = {}
        for result in results:
            d[result['key']] = result['value']

        return d

# - TEST --------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    import doctest
    doctest.testmod()

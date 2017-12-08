from Store import Store

class MemoryStore(Store):
    def __init__(self):
        Store.__init__(self)
        self.database = {}

    def store_record(self, table, record):
        if table not in self.database:
            self.database[table] = {}

        db = self.database[table]
        pk = self.get_primary_key_fields(table)
        pk_values = (record[f] for f in pk)
        db[pk_values] = record

    def get_records(self, table_name, search=None, **kwargs):
        if kwargs:
            if search is None:
                search = kwargs
            else:
                search.update(kwargs)

        if table_name not in self.database:
            self.database[table_name] = {}

        db = self.database[table_name]
        records = []
        if search is None:
            for record in db.values():
                records.append(record)
        else:
            for record in db.values():
                found = True
                for k, v in search.iteritems():
                    if record[k] != v:
                        found = False
                        break
                if found:
                    records.append(record)

        return records

if __name__ == '__main__':
    import pprint

    table_def = {
        'name': "settings",
        "fields": [

            {'name': 'key', 'type': 'char', 'length': 20},
            {'name': 'value', 'type': 'char', 'length': 1000}
        ],
        'primary_key': 'key'
    }

    store = MemoryStore()
    store.register_table(table_def)
    print("PK: %s" % store.get_primary_key_fields('settings'))
    print("fields: %s" % store.get_all_field_names('settings'))
    print("definition:")
    pprint.pprint(store.get_definition('settings'))

    store.store_record('settings', {'key': 'test', 'value': 'aap'})
    store.store_record('settings', {'key': 'other', 'value': 'mies'})

    print(store.get_records('settings'))
    print(store.get_records('settings', {'key': 'other'}))
    print(store.get_records('settings', key='test'))

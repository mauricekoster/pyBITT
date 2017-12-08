
class Store:

    def __init__(self):
        self.registered_tables = {}

    def register_table(self, table_definition):
        name = table_definition['name']
        if name not in self.registered_tables:
            self.registered_tables[name] = table_definition

    def store_record(self, table, record):
        print("Should be overridden")

    def get_records(self, table_name, search):
        print("Should be overridden")

    def get_primary_key_fields(self, table):
        definition = self.registered_tables[table]
        pk_fields = []
        if 'primary_key' in definition:
            pk = definition['primary_key']
            if type(pk) is list:
                pk_fields.extend(pk)
            else:
                pk_fields.append(pk)
        else:
            for field in definition['fields']:
                if 'pk' in field:
                    if field['pk']:
                        pk_fields.append(field['name'])

        return pk_fields

    def get_all_field_names(self, table):
        if table not in self.registered_tables:
            return None

        definition = self.registered_tables[table]
        fields = [fld['name'] for fld in definition['fields']]
        return fields

    def get_definition(self, table):
        if table not in self.registered_tables:
            return None

        return self.registered_tables[table]

if __name__ == '__main__':
    import pprint

    table_def1 = {
        'name': "settings",
        "fields": [

            {'name': 'key', 'type': 'char', 'length': 20},
            {'name': 'value', 'type': 'char', 'length': 1000}
        ],
        'primary_key': 'key'
    }
    table_def2 = {
        'name': "person",
        "fields": [

            {'name': 'id', 'type': 'int', 'pk': True},
            {'name': 'name', 'type': 'char', 'length': 100}
        ]
    }

    store = Store()
    store.register_table(table_def1)
    store.register_table(table_def2)
    print("PK: %s" % store.get_primary_key_fields('settings'))
    print("PK: %s" % store.get_primary_key_fields('person'))
    print("fields: %s" % store.get_all_field_names('person'))
    print("definition:")
    pprint.pprint(store.get_definition('person'))

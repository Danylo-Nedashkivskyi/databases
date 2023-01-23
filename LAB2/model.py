import backend

class Model():
    def __init__(self, table_type):
        self._conn = backend.connect_db()
        self._table_type = table_type
        self._primkey = backend.primkeys[table_type]

    def __del__(self):
        self._conn.commit()
        self._conn.close()

    @property
    def connection(self):
        return self._conn

    @property
    def table_type(self):
        return self._table_type

    def table_type(self, new_table_type):
        if new_table_type not in backend.tables:
            return True
        self._table_type = new_table_type
        return False

    def create_entry(self, args):
        backend.insert_one(self._conn, self._table_type, args)

    def read_entry(self, item):
        return backend.select_one(self._conn, self._table_type, self._primkey, item)

    def read_entries(self):
        return backend.select_all(self._conn, self._table_type)
    
    def update_entry(self, item, args):
        backend.update_one(self._conn, self._table_type, item, args)
    
    def delete_entry(self, item):
        backend.delete_one(self._conn, self._table_type, item)

    def find_entries(self, item, rel):
        return backend.find(self._conn, item, rel)

    def randomize(self, n):
        backend.randomize(self._conn, self._table_type, n)
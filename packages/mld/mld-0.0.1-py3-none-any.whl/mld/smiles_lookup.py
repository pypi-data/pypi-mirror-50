from mld.config import config
import psycopg2 as pgconnector

from mld.configurator import Configurator

configurator = Configurator()


class SmilesLookup:
    def __init__(self):
        self._conn = None
        self._connection_params = config(configurator.get_config_path())

    def connect(self):
        print('Connecting to the database...')
        try:
            conn = pgconnector.connect(**self._connection_params)
            return conn
        except (Exception, pgconnector.DatabaseError) as error:
            print(error)
        finally:
            if self._conn is not None:
                self._conn.close()
                print('Database connection closed.')

    def lookup_by_key(self, drugName):
        if not self._conn:
            self._conn = self.connect()
        try:
            result = []
            cur = self._conn.cursor()

            # execute a statement
            cur.execute("SELECT smiles FROM mld.smiles WHERE drug LIKE '%" + drugName + "%' GROUP BY smiles")
            rows = cur.fetchall()
            for row in rows:
                result.append(row[0])
            cur.close()

            return result
        except (Exception, pgconnector.DatabaseError) as error:
            print(error)
        finally:
            if self._conn is not None:
                self._conn.close()
                print('Database connection closed.')

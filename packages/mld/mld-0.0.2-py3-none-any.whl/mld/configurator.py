import sys
import configparser


class Configurator:

    def __init__(self):
        site_packages = next(p for p in sys.path if 'site-packages' in p)
        self._root_path = site_packages

    def persist(self, host, username, password):
        config = configparser.ConfigParser()
        config['postgresql'] = {'host': host,
                                'database': 'postgres',
                                'user': username,
                                'password': password}
        with open(self.get_config_path(), 'w') as configfile:
            config.write(configfile)

    def get_config_path(self):
        return "{}/{}".format(self._root_path, "db.ini")

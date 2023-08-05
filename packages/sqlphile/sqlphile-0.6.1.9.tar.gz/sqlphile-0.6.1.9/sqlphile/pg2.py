from . import db3
import psycopg2
from .dbtypes import DB_PGSQL, DB_SQLITE3
import sqlphile

class open (db3.open):
    def __init__ (self, dbname, user, password, host = '127.0.0.1', port = 5432, dir = None, auto_reload = False, auto_closing = True):
        if ":" in host:
            host, port = host.split (":")
            port = int (port)
        self.conn = psycopg2.connect (host=host, dbname=dbname, user=user, password=password, port = port)
        self._init (dir, auto_reload, auto_closing, DB_PGSQL)        
        
    def field_names (self):
        return [x.name for x in self.description]
    
    def set_autocommit (self, flag = True):
        self.conn.autocommit = flag


# -----------------------------------------------------------------

class open2 (open, db3.open2):
    def __init__ (self, conn, dir = None, auto_reload = False, auto_closing = True):
        self.conn = conn
        self._init (self, dir, auto_reload, auto_closing, DB_PGSQL)        

# -----------------------------------------------------------------

class open3 (db3.open3):
    def __init__ (self, conn, dir = None, auto_reload = False, auto_closing = True):
        self.conn = conn
        self._init (dir, auto_reload, DB_PGSQL)        

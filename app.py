import os
from socketserver.server import Server
from db.database import Database

INIT_DB = os.getenv('INIT_DB', False)
db = Database('./storage/admissions.db', initialize = INIT_DB)

serv = Server(host='0.0.0.0', port = 80)

serv.post('/query', db.handleGenericQuery)
serv.post('/fetchone', db.handleFetchOneQuery)
serv.post('/fetchmany', db.handleFetchManyQuery)

serv.run()

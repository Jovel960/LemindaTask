from swcdb.thrift import service

DB_CLIENT = None
def initialize():
    global DB_CLIENT
    if DB_CLIENT is None:
        DB_CLIENT = service.Client("localhost",  18000)
    return DB_CLIENT
    #

def get_client(): return DB_CLIENT

def close_connection(): 
    DB_CLIENT.close()

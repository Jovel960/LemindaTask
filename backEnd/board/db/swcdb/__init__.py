from swcdb.thrift import service
from .definer_columns import (QUESTIONS, USER, USER_FEEDBACK)

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


def create_cols():
    DB_CLIENT.sql_mng_column(f"create column(name='QUESTIONS' cid={QUESTIONS} type=SERIAL)")
    DB_CLIENT.sql_mng_column(f"create column(name='USERS'  cid={USER} type=SERIAL)")
    DB_CLIENT.sql_mng_column(f"create column(name='USER_FEEDBACK' CID={USER_FEEDBACK} seq=SERIAL)")



from .definer_columns import (UNIQUE_ID)
from db.swcdb import get_client

def generate_uid(*args):
    ## with SQL:
    key = '[' + ','.join(args) + ']'
    cells = get_client().sql_select_counter(
        f'select where col({UNIQUE_ID})=(cells=(key={key} update=(AUTO,+1)))'
    )
    if len(cells) == 0:
        get_client().sql_update(f'update cell(INSERT,{UNIQUE_ID},{key},"","=1")', 0)
        return 1
    return cells[0].v + 1
    #
from db.swcdb import (get_client)
from .definer_columns import (GENERAL_COMMENT)
from swcdb.thrift.service import (
    UCellSerial,
    CellValueSerial,
    Flag
)

def add_comment(user_id, comment):
     try:
        if (user_has_comment(user_id)):
            return  {'updated': bool(get_client().sql_select_serial(
                f'select where col({GENERAL_COMMENT})=(cells=(key=[="{user_id}"]' +
                f' update~=(AUTO,[0:B:"{comment}"])))'))}
        get_client().update_serial({GENERAL_COMMENT:  [UCellSerial(
            f=Flag.INSERT,
            k=[user_id.encode()],
            v=[CellValueSerial(field_id=0, v_bytes=comment.encode())]
        )]}, 0)
        return {'updated':True}
     except:
         return False

def user_has_comment(user_id):
    return bool(get_client().sql_select_serial(f'select where col({GENERAL_COMMENT})=(cells=(key=[="{user_id}"] limit=1))'))

def delete_general_comment(user_id):
    return {'updated': bool(get_client().sql_select_serial(f'select where col({GENERAL_COMMENT})=(cells=(key=[="{user_id}"] limit=1 DELETE_MATCHING))'))}

def get_comment(user_id):
    user_comment = get_client().sql_select_serial(f'select where col({GENERAL_COMMENT})=(cells=(key=[="{user_id}"] limit=1))')
    return {'user_general_feedback': user_comment[0].v[0].v_bytes.decode()}
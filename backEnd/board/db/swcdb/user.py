from db.swcdb import (get_client)
from .definer_columns import (QUESTIONS,USER,USER_FEEDBACK)
from swcdb.thrift.service import (
    UCellSerial,
    CellValueSerial,
    Flag
)
    #

def register_user(user_id,user_name, pwd):
    #  user_id = str(generate_uid('user_id'))
     get_client().update_serial({USER: [
        UCellSerial(
            f=Flag.INSERT,
            k=[user_id.encode()],
            v=[
                CellValueSerial(field_id=0, v_bytes=user_name.encode()),
                CellValueSerial(field_id=1, v_bytes=pwd.encode()),
            ],
        )
    ]}, 0)
     return True #User created

def remove_user(user_id):
    return  bool(get_client().sql_select(
         f'select where col({USER})=(cells=(key=[={user_id}] limit=1 DELETE_MATCHING))' +
         ' and ' +
         f"col({USER_FEEDBACK})=(cells=(key>=[>'', ={user_id}] DELETE_MATCHING))"))
 
def get_user(user_id):
    user = get_client().sql_select_serial(
        f'select where col({USER})=(cells=(key=[="{user_id}"]))'
    )
    if len(user) == 1:
        return {"user_id":user[0].k[0].decode(),"user_name":user[0].v[0].v_bytes.decode(), "hashed_pwd" : user[0].v[1].v_bytes.decode()}  
    else:
        return False
    

def isUserExists(user_id):
      return len(get_client().sql_select_serial(
        f'select where col({USER})=(cells=(key=[="{user_id}"]))'
    )) == 1      
     
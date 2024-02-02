from db.swcdb import (get_client)
from .definer_columns import (QUESTIONS, UNIQUE_ID,USER,USER_FEEDBACK)
from db.swcdb.common import (generate_uid)
from swcdb.thrift.service import (
    SpecScan,
    UCellSerial,
    CellValueSerial,
    SpecIntervalSerial,
    SpecKeyInterval,
    SpecFraction,
    SpecIntervalOptions,
    Flag,
    Comp,
    SpecColumnSerial,
    SpecFlags,
    SpecFlagsOpt,
    SpecIntervalUpdateSerial,
    SpecUpdateOP,
    UpdateOP,
    SpecValueSerial,
    SpecValueSerialField,
    SpecValueSerial_BYTES,
    CellValueSerialOp,
    FU_BYTES,
    TIMESTAMP_AUTO,
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
            ts_desc=True
        )
    ]}, 0)
     return True #User created

# def remove_user(user_name):
#     pass

def get_user(user_id):
    user = get_client().sql_select_serial(
        f'select where col({USER})=(cells=(key=[="{user_id}"]))'
    )
    print(len(user))
    #print([user[0].k[0].decode(), user[0].v[0].v_bytes.decode()])
    if len(user) == 1:
        return {"user_id":user[0].k[0].decode(),"user_name":user[0].v[0].v_bytes.decode(), "hashed_pwd" : user[0].v[1].v_bytes.decode()}  
    else:
        return False
    

def isUserExists(user_id):
      return len(get_client().sql_select_serial(
        f'select where col({USER})=(cells=(key=[="{user_id}"]))'
    )) == 1      
     
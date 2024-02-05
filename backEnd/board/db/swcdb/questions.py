from db.swcdb import (get_client)
from .definer_columns import (QUESTIONS,USER,USER_FEEDBACK)
from swcdb.thrift.service import (
    UCellSerial,
    CellValueSerial,
    Flag
)
from utilities import (user_operation)

d_questions = [
    {
        "q_id":"1",
        "question": "What is Big O Notation used for?",
        "options": [
            "Calculating the maximum size of a data structure",
            "Measuring the efficiency of an algorithm in terms of time and space",
            "Encrypting data in cybersecurity",
            "Designing user interfaces in software applications"
        ],
        "correct_answer": "Measuring the efficiency of an algorithm in terms of time and space"
    },
    {
        "q_id":"2",
        "question": "Which of the following is a lossless data compression technique?",
        "options": [
            "MPEG",
            "JPEG",
            "Huffman coding",
            "MP3"
        ],
        "correct_answer": "Huffman coding"
    },
    {
        "q_id":"3",
        "question": "What does SQL stand for?",
        "options": [
            "Structured Query Language",
            "Simple Quality Language",
            "Sequential Query List",
            "Standard Query Language"
        ],
        "correct_answer": "Structured Query Language"
    },
    {
        "q_id":"4",
        "question": "Which data structure uses LIFO (Last In, First Out) principle?",
        "options": [
            "Queue",
            "Stack",
            "Array",
            "Linked List"
        ],
        "correct_answer": "Stack"
    },
    {
        "q_id":"5",
        "question": "In object-oriented programming, what does encapsulation refer to?",
        "options": [
            "The process of creating a new class (child) from an existing class (parent)",
            "The bundling of data with the methods that operate on that data",
            "The concept that a class should have only one reason to change",
            "The capability of different classes to use the same interface"
        ],
        "correct_answer": "The bundling of data with the methods that operate on that data"
    },
    {
        "q_id":"6",
        "question": "What is the primary purpose of an operating system?",
        "options": [
            "To provide an environment for a computer user to execute programs",
            "To manage computer hardware and software resources",
            "To protect the computer against viruses",
            "To manage the computer's network connections"
        ],
        "correct_answer": "To manage computer hardware and software resources"
    },
    {
        "q_id":"7",
        "question": "Which of the following is not a programming paradigm?",
        "options": [
            "Object-oriented programming",
            "Functional programming",
            "Procedural programming",
            "Keyword programming"
        ],
        "correct_answer": "Procedural programming"
    },
    {
        "q_id":"8",
        "question": "What does the term 'algorithm' refer to in computer science?",
        "options": [
            "A problem in a computer system",
            "A special type of computer program",
            "A step-by-step procedure for solving a problem or accomplishing some end",
            "A computer's processing speed"
        ],
        "correct_answer": "A special type of computer program"
    },
    {
        "q_id":"9",
        "question": "Which of the following is a characteristic of cloud computing?",
        "options": [
            "Reduced scalability",
            "On-demand self-service",
            "Limited access to resources",
            "Increased operational cost"
        ],
        "correct_answer": "On-demand self-service"
    },
    {
        "q_id":"10",
        "question": "What is a deadlock in the context of operating systems?",
        "options": [
            "A security breach that locks down the system",
            "A situation where two or more processes are unable to proceed because each is waiting for the other to release a resource",
            "A failed process that requires a system restart",
            "An error in the system's registry"
        ],
        "correct_answer": "A situation where two or more processes are unable to proceed because each is waiting for the other to release a resource"
    }
]

def add_questions():
    for q in d_questions:
        get_client().update_serial({QUESTIONS:  [UCellSerial(
        f=Flag.INSERT,
        k=[q["q_id"].encode()],
        v=[
            CellValueSerial(field_id=0, v_bytes=q["question"].encode()),
            CellValueSerial(field_id=1, v_lb=[s.encode() for s in q["options"]]),
            CellValueSerial(field_id=2, v_bytes=q["correct_answer"].encode()),
            ],
        )]}, 0)
    return True

def get_questions(user_id):
    _q = []
    q = get_client().sql_select_serial(f'select where col({QUESTIONS})=(cells=())')
    for __q in q:
        q_id =  __q.k[0].decode()
        question=__q.v[0].v_bytes.decode()
        options = [s.decode() for s in __q.v[1].v_lb]
        correct_answer = __q.v[2].v_bytes.decode()
        user_op = {"rate":"", "feedback":"", "user_ans":""}
        user_r = get_client().sql_select_serial(f'select where col({USER_FEEDBACK})=(cells=(key=[ ="{q_id}", ="{user_id}"]))')
        if(len(user_r)): 
            for field in user_r[0].v:
                if field.field_id == 1:
                    user_op['rate'] = field.v_bytes.decode()  
                elif field.field_id == 0:
                    user_op['feedback'] = field.v_bytes.decode() 
                elif field.field_id == 2:
                    user_op["user_ans"] = field.v_bytes.decode()
        _q.append({
            "q_id": q_id,
            "question": question,
            "options": options,
            "correct_answer": correct_answer,
            "user_answer":"",
            "user_op":user_op,
            }) 
    return _q

def has_q_rating(q_id,user_id):
    has_rating = get_client().sql_select(f'select where col({QUESTIONS})=(cells=(key=[="{q_id}"]  ONLY_KEYS))' + 
                                             ' and ' + f'col({USER_FEEDBACK})=(cells=(key=[="{q_id}", ="{user_id}"]))')
    return len(has_rating.serial_cells) == 2

# def rank(q_id, user_id, rating="", feedback="", user_ans=""):
#      if (has_q_rating(q_id,user_id)):
#          return  {'updated': bool(get_client().sql_select_serial(
#              f'select where col({USER_FEEDBACK})=(cells=(key=[="{q_id}",="{user_id}"]' +
#              f' update~=(AUTO,[1:B:{rating}])))'))}
            
#      get_client().update_serial({USER_FEEDBACK:  [UCellSerial(
#         f=Flag.INSERT,
#         k=[q_id.encode(), user_id.encode()],
#         v=[
#             CellValueSerial(field_id=0, v_bytes=feedback.encode()),
#             CellValueSerial(field_id=1, v_bytes=rating.encode()),
#             CellValueSerial(field_id=2, v_bytes=user_ans.encode()),
#             ],
#         )]}, 0)
#      return {'updated':True}

def user_op(q_id, user_id, feedback="", rating="", user_ans=""):
     if (has_q_rating(q_id,user_id)):
         user_op = user_operation(feedback, rating, user_ans)
         if(user_op):
             return  {'updated': bool(get_client().sql_select_serial(
                 f'select where col({USER_FEEDBACK})=(cells=(key=[="{q_id}",="{user_id}"]' +
                 f' update~=(AUTO,[{user_op[0]}:B:{user_op[1]}])))'))}
         else: return {'updated':False} 
     get_client().update_serial({USER_FEEDBACK:  [UCellSerial(
        f=Flag.INSERT,
        k=[q_id.encode(), user_id.encode()],
        v=[
            CellValueSerial(field_id=0, v_bytes=feedback.encode()),
            CellValueSerial(field_id=1, v_bytes=rating.encode()),
            CellValueSerial(field_id=2, v_bytes=user_ans.encode()),
            ],
        )]}, 0)
     return {'updated':True}

def delete_feedback(q_id, user_id):
    if (has_q_rating(q_id,user_id)):
         return  {'updated': bool(get_client().sql_select_serial(
             f'select where col({USER_FEEDBACK})=(cells=(key=[="{q_id}",="{user_id}"]' +
             f' update~=(AUTO,[0:B:""])))'))}

def get_question_distractors(q_id):
    q = get_client().sql_select_serial(f'select where col({QUESTIONS})=(cells=(key=[={q_id}] limit=1))')
    return [s.decode() for s in q[0].v[1].v_lb]

def remove_all_feedbacks():
    return {'users feedback removed': bool(get_client().sql_select_serial(f'select where col({USER_FEEDBACK})=(cells=(DELETE_MATCHING))'))}
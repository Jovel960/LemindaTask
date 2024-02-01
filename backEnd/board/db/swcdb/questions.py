from db.swcdb import (get_client)
from .definer_columns import (QUESTIONS, UNIQUE_ID,USER,USER_FEEDBACK)
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

def set_questions():
    cellArray = []
    for q in d_questions:
        cellArray += [
            UCellSerial(
            f=Flag.INSERT,
            k=[q.q_id.encode()],
            v=[
                CellValueSerial(field_id=0, v_bytes=q.question.encode()),
                CellValueSerial(field_id=1, v_bytes=q.options[0].encode()),
                CellValueSerial(field_id=1, v_bytes=q.options[1].encode()),
                CellValueSerial(field_id=1, v_bytes=q.options[2].encode()),
                CellValueSerial(field_id=1, v_bytes=q.options[3].encode()),
                CellValueSerial(field_id=1, v_bytes=q.correct_answer.encode()),

            ],
            ts_desc=True
            )
        ]
    return cellArray

def add_questions():
    try:
        cellArray = set_questions()
        for i in range(len(cellArray)):
            get_client().update_serial({QUESTIONS: [
                cellArray[i]
                ]}, 0)
        return True
    except: 
        return False

        
 

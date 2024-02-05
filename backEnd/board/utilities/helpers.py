def user_operation(feedback="", rating="", user_ans=""):
    if bool(feedback):
        return ["0", feedback]
    elif bool(rating):
        return ["1", rating]
    elif bool(user_ans):
        return ["2", user_ans]
    else:
        return False
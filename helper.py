from datetime import datetime


# Create new question with its elements in the data table
# SQL talbe title: ID;Submisson Time;View Number;Vote Number;Title;Message;Image
#
# @req_form: dictionary from html form
def init_question_values(req_form):
    local_time = datetime.now()
    print(local_time)
    view_number = "0"
    vote_number = "0"
    title = req_form["title"]
    data_form_story = req_form["story"]
    image = ""
    new_question = [str(local_time)[:-7], view_number, vote_number,
                    title, data_form_story, image]
    return new_question


# Create new answer with its elements in the data table
# SQL talbe title: ID;Submisson Time;Vote Number;Question ID;Message;Image
#
# @req_form: dictionary from html form
# @question_id: int - index of the question
def init_answer_values(message):
    local_time = datetime.now()
    vote_number = "0"
    new_answer = [str(local_time)[:-7], vote_number, message]
    return new_answer


def init_comment_values(comment, foreign_key):
    entry = {'foreign_key': foreign_key,
             'foreign_key_value': ''}

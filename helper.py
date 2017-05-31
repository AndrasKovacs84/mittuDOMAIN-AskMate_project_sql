from datetime import datetime


# Create new question with its elements in the data table
# SQL table title: ID;Submisson Time;View Number;Vote Number;Title;Message;Image
#
# @req_form: dictionary from html form
def init_question_values(req_form, user_id):
    local_time = datetime.now()
    view_number = "0"
    vote_number = "0"
    title = req_form["title"]
    data_form_story = req_form["story"]
    image = ""
    new_question = [str(local_time)[:-7], view_number, vote_number,
                    title, data_form_story, image, user_id]
    return new_question


# Create new answer with its elements in the data table
# SQL table title: ID;Submisson Time;Vote Number;Question ID;Message;Image
#
# @req_form: dictionary from html form
# @question_id: int - index of the question
def init_answer_values(message):
    local_time = datetime.now()
    vote_number = "0"
    new_answer = [str(local_time)[:-7], vote_number, message]
    return new_answer


# Create new comment with its elements in the data table
# SQL table title: ID,Message;Foreign key;Foreign key value;Submission time
#
# @req_form: dictionary from html form
# @path: list
# @question_id: int - index of the question
def init_comment_values(req_form, path, id):
    comment = {'message': '',
               'foreign_key': '',
               'foreign_key_value': '',
               'submission_time': ''}
    comment['message'] = "'" + str(req_form['comment']).replace("'", "''") + "'"
    print(path)
    if "answer" in path:
        comment['foreign_key'] = 'answer_id'
    if "question" in path:
        comment['foreign_key'] = 'question_id'
    comment['foreign_key_value'] = id
    comment['submission_time'] = "'" + str(datetime.now())[:-7] + "'"

    return comment

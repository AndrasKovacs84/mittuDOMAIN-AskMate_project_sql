import queries
import helper
from flask import Flask, render_template, request, url_for, redirect
from datetime import datetime

app = Flask(__name__)


@app.route('/', methods=['GET'])
def list_questions():
    """ Displays the list of questions.
    Loads data from question table, sorted by time.
    Query can accept a variable to order by, default: sort='submission_time DESC
    """
    questions_table = queries.sql_get_latest_question()
    form_action = '/list'
    button_caption = 'Every question'
    return render_template('list.html', form_action=form_action,
                           questions=questions_table, button_caption=button_caption)


@app.route('/list', methods=['GET'])
def latest_five():
    questions_table = queries.sql_list_questions()
    form_action = '/'
    button_caption = 'Back to index'
    return render_template('list.html', form_action=form_action,
                           questions=questions_table, button_caption=button_caption)


@app.route('/question/new', methods=['GET'])
def new_question():
    """ We arrive here from the list.html "ask question" button.
    Displays an empty question form.
    """
    question = {'result_set': [['', '']]}
    form_action = '/question/new_id'
    button_caption = 'Post Question'
    return render_template('question_form.html', form_action=form_action,
                           question=question, button_caption=button_caption)


@app.route('/question/<int:question_id>', methods=['GET'])
def question(question_id):
    """ Based on the question_id in the url, increases view_count by 1, then a select satement retrieves the
    relevant data for the question with the id. Another query collects all the associated answers, then the
    page is rendered with the two parts.
    """
    queries.sql_update_question_view_count(question_id)
    question_comments = queries.sql_gather_question_comments(question_id)
    answers = queries.sql_answers_to_question(question_id)
    selected_question = queries.sql_question_details(question_id)
    print(answers)
    return render_template('question_details.html', question=selected_question, question_id=question_id, answers=answers, question_comments=question_comments)


@app.route('/question/<int:question_id>', methods=['POST'])
def update_question(question_id):
    question_to_update = {'id': None,
                          'title': None,
                          'message': None}
    question_to_update['id'] = question_id
    question_to_update['title'] = "'" + request.form['title'].replace("'", "''") + "'"
    question_to_update['message'] = "'" + request.form['story'].replace("'", "''") + "'"
    queries.sql_update_question_details(question_to_update)
    return redirect('/question/' + str(question_id))


@app.route('/question/<int:question_id>/new_answer', methods=['GET'])
def new_answer_form(question_id):
    """ Displays empty form for entering an answer to the selected question (also displays question title on top).
    We arrive here from '/question/question_id/'
    """
    return render_template('answer_form.html',
                           question=queries.sql_get_question_text(question_id), question_id=question_id)


@app.route('/answer/new_id', methods=['POST'])
def new_answer_id():
    """ Adds new answer to the answer table
    """
    button_value = request.form["button"]
    new_row = helper.init_answer_values(request.form["answer"])
    queries.sql_insert_answer(new_row, button_value)
    return redirect("/question/" + button_value)


@app.route('/question/new_id', methods=['POST'])
def new_question_id():
    button_value = request.form["button"]
    if button_value == "Post Question":
        new_question = helper.init_question_values(request.form)
        new_question_id = queries.sql_insert_new_question(new_question)
        # TODO: is this still needed?
        print(new_question)
        return redirect("/question/" + str(int(new_question_id)))


@app.route('/question/<int:question_id>/delete', methods=['POST'])
def delete_question(question_id):
    queries.sql_delete_question_tag(question_id)
    queries.sql_delete_comment(question_id)
    queries.sql_delete_answer(question_id)
    queries.sql_delete_question(question_id)
    return redirect("/")


@app.route('/question/<int:question_id>/edit', methods=['GET'])
def edit_question_form(question_id):
    question = queries.sql_question_details(question_id)
    form_action = '/question/' + str(question_id)
    button_caption = 'Update Question'
    print(question)
    return render_template("question_form.html", question=question, form_action=form_action, button_caption=button_caption)


@app.route('/question/<question_id>/new-comment', methods=['GET'])
def add_comment_to_question(question_id):
    question = queries.sql_question_details(question_id)
    question['type'] = 'question'
    return render_template('comment_form.html', data=question)


@app.route('/question/<question_id>/add_comment', methods=['POST'])
def insert_question_comment(question_id):
    comment = {'message': '',
               'foreign_key': '',
               'foreign_key_value': '',
               'submission_time': ''}
    comment['message'] = "'" + str(request.form['comment']).replace("'", "''") + "'"
    comment['foreign_key'] = 'question_id'
    comment['foreign_key_value'] = question_id
    comment['submission_time'] = "'" + str(datetime.now())[:-7] + "'"
    queries.sql_insert_comment(comment)
    return redirect('/question/' + str(question_id))


@app.route('/answer/<answer_id>/new-comment', methods=['GET'])
def add_comment_to_answer(answer_id):
    answer = queries.sql_answer_details(answer_id)
    answer['type'] = 'answer'
    print(answer)
    return render_template('comment_form.html', data=answer)


@app.route('/answer/<answer_id>/add_comment', methods=['POST'])
def insert_answer_comment(answer_id):
    comment = {'message': '',
               'foreign_key': '',
               'foreign_key_value': '',
               'submission_time': ''}
    comment['message'] = "'" + str(request.form['comment']).replace("'", "''") + "'"
    comment['foreign_key'] = 'answer_id'
    comment['foreign_key_value'] = answer_id
    comment['submission_time'] = "'" + str(datetime.now())[:-7] + "'"
    queries.sql_insert_comment(comment)
    answer = queries.sql_answer_details(answer_id)
    return redirect('/question/' + str(answer['question_id']))


if __name__ == '__main__':
    app.run(debug=True)

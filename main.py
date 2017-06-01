import helper
from data_access import user_queries, multi_table_queries, question_queries, answer_queries, comment_queries, tag_queries
from data_access.server_connection import connect
from flask import Flask, render_template, request, url_for, redirect, abort
from datetime import datetime

app = Flask(__name__)


@app.route('/', methods=['GET'])
def display_list_of_questions():
    """ Displays the list of questions.
    Loads data from question table, sorted by time.
    Query can accept a variable to order by, default: sort='submission_time DESC
    """
    questions_table = multi_table_queries.get_latest_question()
    form_action = '/list'
    button_caption = 'Every question'
    return render_template('list.html',
                           form_action=form_action,
                           questions=questions_table,
                           button_caption=button_caption
                           )


@app.route('/list', methods=['GET'])
def latest_five():
    questions_table = multi_table_queries.list_questions()
    form_action = '/'
    button_caption = 'Back to index'
    return render_template('list.html',
                           form_action=form_action,
                           questions=questions_table,
                           button_caption=button_caption
                           )


@app.route('/question/new', methods=['GET'])
def new_question():
    """ We arrive here from the list.html "ask question" button.
    Displays an empty question form.
    """
    question = {'result_set': [['', '']]}
    form_action = '/question/new_id'
    button_caption = 'Post Question'
    usernames = user_queries.get_usernames()
    return render_template('question_form.html',
                           form_action=form_action,
                           question=question,
                           button_caption=button_caption,
                           usernames=usernames
                           )


@app.route('/question/<int:question_id>', methods=['GET'])
def question(question_id):
    """ Based on the question_id in the url, increases view_count by 1, then a select satement retrieves the
    relevant data for the question with the id. Another query collects all the associated answers, then the
    page is rendered with the two parts.
    """
    question_queries.update_question_view_count(question_id)
    question_comments = multi_table_queries.gather_question_comments(question_id)
    answers = multi_table_queries.answers_to_question(question_id)
    selected_question = question_queries.question_details(question_id)
    author = user_queries.get_usernames(question_id)
    return render_template('question_details.html',
                           question=selected_question,
                           question_id=question_id,
                           answers=answers,
                           question_comments=question_comments,
                           author=author
                           )


@app.route('/question/<int:question_id>', methods=['POST'])
def update_question(question_id):
    question_to_update = {'id': None,
                          'title': None,
                          'message': None}
    question_to_update['id'] = question_id
    question_to_update['title'] = request.form['title']
    question_to_update['message'] = request.form['story']
    question_queries.update_question_details(question_to_update)
    return redirect('/question/' + str(question_id))


@app.route('/question/<int:question_id>/new_answer', methods=['GET'])
def new_answer_form(question_id):
    """ Displays empty form for entering an answer to the selected question (also displays question title on top).
    We arrive here from '/question/question_id/'
    """
    usernames = user_queries.get_usernames()
    return render_template('answer_form.html',
                           question=question_queries.get_question_text(question_id),
                           question_id=question_id,
                           usernames=usernames
                           )


@app.route('/answer/new_id', methods=['POST'])
def new_answer_id():
    """ Adds new answer to the answer table
    """
    user_id = user_queries.get_user_id(request.form["selected_user"])[0][0]
    button_value = request.form["button"]
    new_answer = helper.init_answer_values(request.form["answer"], user_id)
    answer_queries.insert_answer(new_answer, button_value)
    return redirect("/question/" + button_value)


@app.route('/question/new_id', methods=['POST'])
def new_question_id():
    """ Handles the post request of the new question form
    """
    user_id = user_queries.get_user_id(request.form["selected_user"])[0][0]
    button_value = request.form["button"]
    if button_value == "Post Question":
        new_question = helper.init_question_values(request.form, user_id)
        new_question_id = question_queries.insert_new_question(new_question)
        return redirect("/question/" + str(int(new_question_id)))


@app.route('/question/<int:question_id>/delete', methods=['POST'])
def delete_question(question_id):
    tag_queries.delete_question_tag(question_id)
    comment_queries.delete_comment('question_id', question_id)
    answers = multi_table_queries.answers_to_question(question_id)
    for answer_with_comments in answers['result_set']:
        for comment in answer_with_comments['comments']:
            comment_queries.delete_comment('id', comment[0])
    answer_queries.delete_answer(question_id)
    question_queries.delete_question(question_id)
    return redirect("/")


@app.route('/question/<int:question_id>/edit', methods=['GET'])
def edit_question_form(question_id):
    """ Edits the question form
    """
    question = question_queries.question_details(question_id)
    form_action = '/question/' + str(question_id)
    button_caption = 'Update Question'
    return render_template("question_form.html",
                           question=question,
                           form_action=form_action,
                           button_caption=button_caption
                           )


@app.route('/question/<int:question_id>/new-comment', methods=['GET'])
def add_comment_to_question(question_id):
    question = question_queries.question_details(question_id)
    question['type'] = 'question'
    usernames = user_queries.get_usernames()
    return render_template('comment_form.html',
                           data=question,
                           usernames=usernames)


@app.route('/question/<int:question_id>/add_comment', methods=['POST'])
def insert_question_comment(question_id):
    user_id = user_queries.get_user_id(request.form["selected_user"])[0][0]
    comment = helper.init_comment_values(request.form, request.path, question_id)
    comment_queries.insert_comment(comment, user_id)
    return redirect('/question/' + str(question_id))


@app.route('/answer/<int:answer_id>/new-comment', methods=['GET'])
def add_comment_to_answer(answer_id):
    answer = answer_queries.answer_details(answer_id)
    answer['type'] = 'answer'
    usernames = user_queries.get_usernames()
    return render_template('comment_form.html',
                           data=answer,
                           usernames=usernames)


@app.route('/answer/<int:answer_id>/add_comment', methods=['POST'])
def insert_answer_comment(answer_id):
    user_id = user_queries.get_user_id(request.form["selected_user"])[0][0]
    comment = helper.init_comment_values(request.form, request.path, answer_id)
    comment_queries.insert_comment(comment, user_id)
    answer = answer_queries.answer_details(answer_id)
    return redirect('/question/' + str(answer['question_id']))


@app.route('/users/<int:user_id>', methods=['GET'])
def user_activities(user_id):
    user_data = {'name': '',
                 'reputation': '',
                 'submission_time': ''}
    user_activities = {'questions': [],
                       'answers': [],
                       'comments': []}
    user_data = user_queries.get_user_data_of_id(user_id)
    user_activities = multi_table_queries.get_user_activities_of_id(user_id)
    return render_template('user_activities.html', user_data=user_data,
                           user_activities=user_activities)


@app.route('/registration', methods=['GET'])
def new_user_form():
    """ We arrive here from the index.html "Registration" button.
    Displays an empty user form.
    """
    name_exist = ""
    if "messages" in request.args:
        name_exist = request.args['messages']
    form_action = '/registration/new_user'
    button_caption = 'Submit Registration'
    return render_template('user_form.html',
                           name_exist=name_exist,
                           form_action=form_action,
                           button_caption=button_caption
                           )


@app.route('/registration/new_user', methods=['POST'])
def insert_user():
    """ We arrive here from the user_form.html "Submit Registration" button.
    Inicializing user data, end returning to index page. (In future to user page.)
    """
    user = helper.init_user_values(request.form)
    insertion = user_queries.sql_insert_user(user)
    # user_mate = user_queries.sql_select_user(answer_id)
    if not insertion:
        messages = "User name already exists!"
        return redirect(url_for('new_user_form', messages=messages))
    else:
        return redirect('/')


@app.route('/users', methods=['GET'])
def list_users():
    questions_table = user_queries.list_users()
    form_action = '/'
    button_caption = 'Back to index'
    return render_template('user_list.html',
                           form_action=form_action,
                           questions=questions_table,
                           button_caption=button_caption
                           )


@app.route('/question/<int:question_id>/vote-up', methods=['POST'])
def question_vote_up(question_id):
    vote_change = '+1'
    reputation_change = '+5'
    table = 'question'
    user_queries.update_reputation(table, question_id, reputation_change)
    multi_table_queries.update_vote_nr(table, question_id, vote_change)
    return redirect('/question/' + str(question_id))


@app.route('/question/<int:question_id>/vote-down', methods=['POST'])
def question_vote_down(question_id):
    vote_change = '-1'
    table = 'question'
    reputation_change = '-2'
    user_queries.update_reputation(table, question_id, reputation_change)
    multi_table_queries.update_vote_nr(table, question_id, vote_change)
    return redirect('/question/' + str(question_id))


@app.route('/answer/<int:answer_id>/vote-up', methods=['POST'])
def answer_vote_up(answer_id):
    vote_change = '+1'
    table = 'answer'
    reputation_change = '+10'
    answer = answer_queries.answer_details(answer_id)
    user_queries.update_reputation(table, answer_id, reputation_change)
    multi_table_queries.update_vote_nr(table, answer_id, vote_change)
    return redirect('/question/' + str(answer['question_id']))


@app.route('/answer/<int:answer_id>/vote-down', methods=['POST'])
def answer_vote_down(answer_id):
    vote_change = '-1'
    table = 'answer'
    reputation_change = '-2'
    answer = answer_queries.answer_details(answer_id)
    user_queries.update_reputation(table, answer_id, reputation_change)
    multi_table_queries.update_vote_nr(table, answer_id, vote_change)
    return redirect('/question/' + str(answer['question_id']))


@app.route('/answer/<int:answer_id>', methods=['GET'])
def comment_to_answer_to_question(answer_id):
    answer = answer_queries.answer_details(answer_id)
    return redirect('/question/' + str(answer['question_id']))


@app.errorhandler(TypeError)
def server_side_type_error(e):
    print(e)
    return render_template('500.html'), 500


@app.errorhandler(AttributeError)
def server_side_attribute_error(e):
    print(e)
    return render_template('500.html'), 500


@app.errorhandler(NameError)
def user_side_name_error(e):
    print(e)
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)

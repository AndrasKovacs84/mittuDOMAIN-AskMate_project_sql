import select_queries
import delete_queries
import insert_queries
import user_queries
import helper
from flask import Flask, render_template, request, url_for, redirect, abort
from datetime import datetime

app = Flask(__name__)


@app.route('/', methods=['GET'])
def list_questions():
    """ Displays the list of questions.
    Loads data from question table, sorted by time.
    Query can accept a variable to order by, default: sort='submission_time DESC
    """
    questions_table = select_queries.sql_get_latest_question()
    form_action = '/list'
    button_caption = 'Every question'
    return render_template('list.html',
                           form_action=form_action,
                           questions=questions_table,
                           button_caption=button_caption
                           )


@app.route('/list', methods=['GET'])
def latest_five():
    questions_table = select_queries.sql_list_questions()
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
    usernames = select_queries.sql_get_usernames()
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
    select_queries.sql_update_question_view_count(question_id)
    question_comments = select_queries.sql_gather_question_comments(question_id)
    answers = select_queries.sql_answers_to_question(question_id)
    selected_question = select_queries.sql_question_details(question_id)
    user = select_queries.sql_get_usernames(question_id)
    return render_template('question_details.html',
                           question=selected_question,
                           question_id=question_id,
                           answers=answers,
                           question_comments=question_comments,
                           user=user
                           )


@app.route('/question/<int:question_id>', methods=['POST'])
def update_question(question_id):
    question_to_update = {'id': None,
                          'title': None,
                          'message': None}
    question_to_update['id'] = question_id
    question_to_update['title'] = "'" + request.form['title'].replace("'", "''") + "'"
    question_to_update['message'] = "'" + request.form['story'].replace("'", "''") + "'"
    select_queries.sql_update_question_details(question_to_update)
    return redirect('/question/' + str(question_id))


@app.route('/question/<int:question_id>/new_answer', methods=['GET'])
def new_answer_form(question_id):
    """ Displays empty form for entering an answer to the selected question (also displays question title on top).
    We arrive here from '/question/question_id/'
    """
    usernames = select_queries.sql_get_usernames()
    return render_template('answer_form.html',
                           question=select_queries.sql_get_question_text(question_id),
                           question_id=question_id,
                           usernames=usernames
                           )


@app.route('/answer/new_id', methods=['POST'])
def new_answer_id():
    """ Adds new answer to the answer table
    """
    user_id = select_queries.sql_get_user_id(request.form["selected_user"])[0][0]
    button_value = request.form["button"]
    new_answer = helper.init_answer_values(request.form["answer"], user_id)
    insert_queries.sql_insert_answer(new_answer, button_value)
    return redirect("/question/" + button_value)


@app.route('/question/new_id', methods=['POST'])
def new_question_id():
    """ Handles the post request of the new question form
    """
    user_id = select_queries.sql_get_user_id(request.form["selected_user"])[0][0]
    button_value = request.form["button"]
    if button_value == "Post Question":
        new_question = helper.init_question_values(request.form, user_id)
        new_question_id = insert_queries.sql_insert_new_question(new_question)
        return redirect("/question/" + str(int(new_question_id)))


@app.route('/question/<int:question_id>/delete', methods=['POST'])
def delete_question(question_id):
    delete_queries.sql_delete_question_tag(question_id)
    delete_queries.sql_delete_comment('question_id', question_id)
    answers = select_queries.sql_answers_to_question(question_id)
    for answer_with_comments in answers['result_set']:
        for comment in answer_with_comments['comments']:
            delete_queries.sql_delete_comment('id', comment[0])
    delete_queries.sql_delete_answer(question_id)
    delete_queries.sql_delete_question(question_id)
    return redirect("/")


@app.route('/question/<int:question_id>/edit', methods=['GET'])
def edit_question_form(question_id):
    """ Edits the question form
    """
    question = select_queries.sql_question_details(question_id)
    form_action = '/question/' + str(question_id)
    button_caption = 'Update Question'
    return render_template("question_form.html",
                           question=question,
                           form_action=form_action,
                           button_caption=button_caption
                           )


@app.route('/question/<int:question_id>/new-comment', methods=['GET'])
def add_comment_to_question(question_id):
    question = select_queries.sql_question_details(question_id)
    question['type'] = 'question'
    usernames = select_queries.sql_get_usernames()
    return render_template('comment_form.html',
                           data=question,
                           usernames=usernames)


@app.route('/question/<int:question_id>/add_comment', methods=['POST'])
def insert_question_comment(question_id):
    user_id = select_queries.sql_get_user_id(request.form["selected_user"])[0][0]
    comment = helper.init_comment_values(request.form, request.path, question_id)
    insert_queries.sql_insert_comment(comment, user_id)
    return redirect('/question/' + str(question_id))


@app.route('/answer/<int:answer_id>/new-comment', methods=['GET'])
def add_comment_to_answer(answer_id):
    answer = select_queries.sql_answer_details(answer_id)
    answer['type'] = 'answer'
    usernames = select_queries.sql_get_usernames()
    return render_template('comment_form.html',
                           data=answer,
                           usernames=usernames)


@app.route('/answer/<int:answer_id>/add_comment', methods=['POST'])
def insert_answer_comment(answer_id):
    user_id = select_queries.sql_get_user_id(request.form["selected_user"])[0][0]
    comment = helper.init_comment_values(request.form, request.path, answer_id)
    insert_queries.sql_insert_comment(comment, user_id)
    answer = select_queries.sql_answer_details(answer_id)
    return redirect('/question/' + str(answer['question_id']))


@app.route('/users/<int:user_id>', methods=['GET'])
def user_activities(user_id):
    user_data = {'name': '',
                 'reputation': '',
                 'submission_time': ''}
    user_activities = {'questions': [],
                       'answers': [],
                       'comments': []}
    user_data = select_queries.sql_get_user_data_of_id(user_id)
    user_activities = select_queries.sql_get_user_activities_of_id(user_id)
    return render_template('user_activities.html', user_data=user_data,
                           user_activities=user_activities)


@app.route('/registration', methods=['GET'])
def new_user_form():
    """ We arrive here from the index.html "Registration" button.
    Displays an empty user form.
    """
    form_action = '/registration/new_user'
    button_caption = 'Submit Registration'
    return render_template('user_form.html',
                           form_action=form_action,
                           button_caption=button_caption
                           )


@app.route('/registration/new_user', methods=['POST'])
def insert_user():
    """ We arrive here from the user_form.html "Submit Registration" button.
    Inicializing user data, end returning to index page. (In future to user page.)
    """
    user = helper.init_user_values(request.form)
    user_queries.sql_insert_user(user)
    # user_mate = user_queries.sql_select_user(answer_id)
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
    change = '+1'
    table = 'question'
    insert_queries.sql_update_vote_nr(table, question_id, change)
    return redirect('/question/' + str(question_id))


@app.route('/question/<int:question_id>/vote-down', methods=['POST'])
def question_vote_down(question_id):
    change = '-1'
    table = 'question'
    insert_queries.sql_update_vote_nr(table, question_id, change)
    return redirect('/question/' + str(question_id))


@app.route('/answer/<int:answer_id>/vote-up', methods=['POST'])
def answer_vote_up(answer_id):
    change = '+1'
    table = 'answer'
    answer = select_queries.sql_answer_details(answer_id)
    insert_queries.sql_update_vote_nr(table, answer_id, change)
    return redirect('/question/' + str(answer['question_id']))


@app.route('/answer/<int:answer_id>/vote-down', methods=['POST'])
def answer_vote_down(answer_id):
    change = '-1'
    table = 'answer'
    answer = select_queries.sql_answer_details(answer_id)
    insert_queries.sql_update_vote_nr(table, answer_id, change)
    return redirect('/question/' + str(answer['question_id']))


@app.errorhandler(TypeError)
def server_side_type_error(e):
    return render_template('500.html'), 500


@app.errorhandler(AttributeError)
def server_side_attribute_error(e):
    return render_template('500.html'), 500


@app.errorhandler(NameError)
def user_side_name_error():
    return render_template('404.html'), 404


#@app.route('/', methods=['GET'])
#def user_details(id):
 #   user_queries.sql_user_details(id)
    
  #  form_action = '/'
   # button_caption = 'Home'
    #return render_template('user_detail_list.html',
     #                      form_action=form_action,
      #                     button_caption=button_caption
       #                    )








if __name__ == '__main__':
    app.run(debug=True)

import queries
import helper
from flask import Flask, render_template, request, url_for, redirect


app = Flask(__name__)


@app.route('/', methods=['GET'])
def list_questions():
    ''' Displays the list of questions.
    Loads data from question table, sorted by time.'''
    questions_table = queries.sql_list_questions()  # Query can accept a variable to order by, default: sort='submission_time DESC'
    return render_template('list.html', questions=questions_table)


@app.route('/question/new', methods=['GET'])
def new_question():
    """
    We arrive here from the list.html "ask question" button.
    Displays an empty question form.
    """
    question = {'result_set': [['', '']]}
    form_action = '/question/new_id'
    button_caption = 'Post Question'
    return render_template('question_form.html', form_action=form_action,
                           question=question, button_caption=button_caption)


@app.route('/question/<int:question_id>', methods=['GET'])
def question(question_id):
    """Based on the question_id in the url, increases view_count by 1, then a select satement retrieves the
    relevant data for the question with the id. Another query collects all the associated answers, then the
    page is rendered with the two parts."""
    queries.sql_update_question_view_count(question_id)
    question_comments = queries.sql_gather_question_comments(question_id)
    answers = queries.sql_answers_to_question(question_id)
    # answer_comments = queries.sql_gather_answer_comments(answer_id_list)
    selected_question = queries.sql_question_details(question_id)
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
    ''' Displays empty form for entering an answer to the selected question (also displays question title on top).
    We arrive here from '/question/question_id/' '''

    query = 'SELECT title, message FROM question WHERE id = ' + str(question_id) + ';'
    question_overview = queries.sql_empty_qry(query)['result_set'][0]
    return render_template('answer_form.html', question=question_overview, question_id=question_id)


@app.route('/answer/new_id', methods=['POST'])
def new_answer_id():
    ''' Adds new answer to the answer table'''
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
        print(new_question)
        return redirect("/question/" + str(int(new_question_id)))


@app.route('/question/<int:question_id>/delete', methods=['POST'])
def delete_question(question_id):
    queries.sql_delete(question_id)
    queries.sql_delete_answer(question_id)
    queries.sql_delete_comment(question_id)
    return redirect("/")


@app.route('/question/<int:question_id>/edit', methods=['GET'])
def edit_question_form(question_id):
    id_query = "SELECT title, message FROM question WHERE id=(%s);" % (question_id)
    question = queries.sql_empty_qry(id_query)
    form_action = '/question/' + str(question_id)
    button_caption = 'Update Question'
    return render_template("question_form.html", question=question, form_action=form_action, button_caption=button_caption)


if __name__ == '__main__':
    app.run(debug=True)

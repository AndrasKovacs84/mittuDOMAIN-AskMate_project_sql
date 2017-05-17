import queries
import common
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
    question = dict()
    form_action = '/question/new_id'
    button_caption = 'Post Question'
    return render_template('question_form.html', form_action=form_action,
                           question=question, button_caption=button_caption)


@app.route('/question/<int:question_id>')
def question(question_id, methods=['GET']):
    """Based on the question_id in the url, increases view_count by 1, then a select satement retrieves the
    relevant data for the question with the id. Another query collects all the associated answers, then the
    page is rendered with the two parts."""
    queries.sql_update_question_view_count(question_id)
    selected_question = queries.sql_question_details(question_id)
    answers = queries.sql_answers_to_question(question_id)
    return render_template('question_details.html', question=selected_question, answers=answers)


@app.route('/question/<int:question_id>/new_answer', methods=['GET'])
def new_answer_form(question_id):
    ''' Displays empty form for entering an answer to the selected question (also displays question title on top).
    We arrive here from '/question/question_id/' '''

    query = 'SELECT title, message FROM question WHERE id = ' + str(question_id) + ';'
    question_title = queries.sql_empty_qry(query)['result_set'][0]
    return render_template('answer_form.html', question=question_title, question_id=question_id)


@app.route('/question/new_id', methods=['POST'])
def new_question_id():
    button_value = request.form["button"]
    if button_value == "Post Question":
        new_question = common.get_new_question_values(request.form)
        data_to_insert = {'table': 'tablename', 
                          'columns': ['submission_time', 'view_number', 'vote_number', 'title', 'message', 'image'], 
                          'values': new_question}
        queries.sql_insert(data_to_insert)
        id_query = "SELECT max(id) FROM question;"
        new_question = queries.sql_empty_qry(id_query)
        print(new_question)
        return redirect("/question/" + str(int(new_question['result_set'][0][0])))
    if button_value.isdigit():
        data = data_manager.get_datatable_from_file('data/answer.csv', ANSWER_B64_COL)
        new_answer = common.get_new_answer(data, request.form, button_value)
        return redirect("/question/" + button_value)


@app.route('/question/<int:question_id>/delete', methods=['GET'])
def delete_question(question_id):
    common.delete_data_by_id('data/question.csv', question_id, QUESTION_B64_COL, 0)
    common.delete_data_by_id('data/answer.csv', question_id, ANSWER_B64_COL, 3)
    return redirect("/")


@app.route('/question/<int:question_id>/edit', methods=['GET'])
def edit_question_form(question_id):
    id_query = "SELECT title, message FROM question WHERE id=(%s);" % (question_id)
    question = queries.sql_empty_qry(id_query)
    form_action = '/question/' + str(question_id)
    button_caption = 'Update Question'
    return render_template("question_form.html", question=question, form_action=form_action, button_caption=button_caption)


@app.route('/question/<int:question_id>', methods=['POST'])
def update_question(question_id):
    questions = data_manager.get_datatable_from_file('data/question.csv', QUESTION_B64_COL)
    for question in questions:
        if question[0] == str(question_id):
            question[4] = request.form["title"]
            question[5] = request.form['story']
            break
    data_manager.write_datatable_to_file('data/question.csv', questions, QUESTION_B64_COL)
    return redirect('/question/' + str(question_id))


if __name__ == '__main__':
    app.run(debug=True)

from server_connection.connect import connect_to_sql


@connect_to_sql
def answer_details(cursor, answer_id):
    cursor.execute("""
                   SELECT
                   id AS "Id",
                   submission_time AS "Submission time",
                   vote_number AS "Vote number",
                   question_id AS "Question id",
                   message AS "Message",
                   image AS "Image"
                   FROM answer
                   WHERE id={0}
                   """.format(answer_id))
    result = cursor.fetchall()
    answer = {'id': result[0][0],
              'submission_time': result[0][1],
              'vote_number': result[0][2],
              'question_id': result[0][3],
              'message': result[0][4],
              'image': result[0][5]}
    return answer


@connect_to_sql
def delete_answer(cursor, question_id,):
    cursor.execute(""" DELETE FROM answer WHERE question_id = '{0}'; """.format(question_id))


@connect_to_sql
def insert_answer(cursor, init_answer, question_id):
    cursor.execute("""
                   INSERT INTO answer (submission_time, vote_number, question_id, message, user_mates_id)
                   VALUES ('{0}', '{1}', (SELECT id FROM question WHERE id='{2}'),'{3}', {4});
                   """.format(init_answer[0], init_answer[1], question_id, init_answer[2], init_answer[3]))

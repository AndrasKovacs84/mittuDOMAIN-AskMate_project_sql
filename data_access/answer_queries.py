from .server_connection.connect import connect_to_sql


@connect_to_sql
def answer_details(cursor, answer_id):
    query = """
            SELECT
            id AS "Id",
            submission_time AS "Submission time",
            vote_number AS "Vote number",
            question_id AS "Question id",
            message AS "Message",
            image AS "Image"
            FROM answer
            WHERE id=%s
            """
    cursor.execute(query, (answer_id,))
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
    statement = """ DELETE FROM answer WHERE question_id = %s; """
    cursor.execute(statement, (question_id,))


@connect_to_sql
def insert_answer(cursor, init_answer, question_id):
    statement = """
                INSERT INTO answer (submission_time, vote_number, question_id, message, user_mates_id)
                VALUES (%s, %s, (SELECT id FROM question WHERE id=%s), %s, %s);
                """
    cursor.execute(statement, (init_answer[0], init_answer[1], question_id, init_answer[2], init_answer[3]))
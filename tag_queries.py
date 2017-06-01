from connect import connect_to_sql

@connect_to_sql
def list_tag(cursor):
    data = {'result_set': []}
    cursor.execute("""SELECT name FROM tag """)
    rows = cursor.fetchall()
    data['result_set'] = rows
    return data







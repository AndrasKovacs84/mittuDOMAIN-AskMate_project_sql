from connect import connect_to_sql


@connect_to_sql
def select_statement(query):
    '''Displays the query chosen by the user. Parameter is a dictionary of the relevant properties
    for a simple query. Returns the results of the query. data[0] = list of column names as header,
    data[1] = list of lists, where each nested list represents a row of data.'''
    data = []
    cursor.execute("""
                   SELECT DISTINCT {1}
                   FROM {0}
                   WHERE {2}
                   ORDER BY {3};
                   """.format(query['table'], ", ".join(query['columns']), query['filter'], query['order_by']))
    column_names = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    data.append(column_names)
    data.append(rows)
    return data



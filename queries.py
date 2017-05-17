from connect import connect_to_sql


@connect_to_sql
def sql_select(query):
    '''Displays the query chosen by the user. Parameter is a dictionary of the relevant properties
    for a simple query. Returns the results of the query. data[0] = list of column names as header,
    data[1] = list of lists, where each nested list represents a row of data.'''
    data = {'header': [],
            'result_set':[]}
    cursor.execute("""
                   SELECT DISTINCT {1}
                   FROM {0}
                   WHERE {2}
                   ORDER BY {3};
                   """.format(query['table'], ", ".join(query['columns']), query['filter'], query['order_by']))
    column_names = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    data['header'] = column_names
    data['result_set'] = rows
    return data


@connect_to_sql
def sql_insert():
    ''''''
    pass


@connect_to_sql
def sql_update():
    cur.execute(""" UPDATE {1}
                     SET {2}
                     WHERE {3}; 
                     """.format(query['table']))


@connect_to_sql
def sql_delete():
    cur.execute(""" DELETE FROM {1}
                    WHERE {2}
                """.format(data_to_delete['table']), data_to_delete['filter']))

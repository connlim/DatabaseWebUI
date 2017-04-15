from flask import Flask, request, session, g, redirect, url_for, abort, render_template, jsonify
from sqlalchemy import create_engine, MetaData, Table
import numbers


# SQL error exception
class SQLError(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


app = Flask(__name__)
# Load config
app.config.update(
    DEBUG='True',
    MYSQL_DATABASE_HOST='127.0.0.1',
    MYSQL_DATABASE_PORT=3306,
    MYSQL_DATABASE_USER='root',
    MYSQL_DATABASE_DB='pe'
)
engine = create_engine('mysql://root:@localhost/pe', convert_unicode=True)
metadata = MetaData(bind=engine)


# Default search route
@app.route('/')
@app.route('/search', methods=['GET'])
def search():
    return render_template('search.html')


# Handle form input from search
@app.route('/search', methods=['POST'])
def search_post():
    # Sort by search criteria
    if request.form.get('use_student') and request.form.get('use_exercise'): # Search criteria from both tables
        # Create dictionaries of the search criteria
        student_details = {'id': request.form.get('student_id'), 'weight': request.form.get('weight'), 
                            'height': request.form.get('height'), 'sex': request.form.get('sex')}
        exercise_details = {'name': request.form.get('exercise_name'), 'type': request.form.get('type'), 
                            'intensity': request.form.get('intensity')}
        # Display the query result
        result = queryDoubleTables(student_details, exercise_details)
        return render_template('browse.html', title='Search Results', entries=[result], table_names=['tested'])
    elif request.form.get('use_student'): # Search criteria from student table
        student_details = {'id': request.form.get('student_id'), 'weight': request.form.get('weight'), 
                            'height': request.form.get('height'), 'sex': request.form.get('sex')}
        result = querySingleTable('student', student_details)
        return render_template('browse.html', title='Search Results', entries=[result], table_names=['tested'])
    elif request.form.get('use_exercise'):
        exercise_details = {'name': request.form.get('exercise_name'), 'type': request.form.get('type'), 
                            'intensity': request.form.get('intensity')}
        result = querySingleTable('exercise', exercise_details)
        return render_template('browse.html', title='Search Results', entries=[result], table_names=['tested'])
    else: # Default, no criteria
        result = queryTested()
        return render_template('browse.html', title='All Records (no criteria selected)', entries=[result], table_names=['tested'])
        

@app.route('/browse')
def browse():
    try:
        connection = engine.connect()
        result = []
        table_names = []
        # Get results from each table
        tables = connection.execute('show tables')
        for table_name in tables:
            result.append(connection.execute('SELECT * FROM ' + table_name[0]))
            table_names.append(table_name[0])
        connection.close()
        return render_template('browse.html', title='Browse', entries=result, table_names=table_names)
    except Exception as e:
        raise SQLError(repr(e))
        

# Handle any SQLErrors that are raised throughout the app
@app.errorhandler(SQLError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


# Handle queries involving criteria in both tables
def queryDoubleTables(student_details, exercise_details):
    # Starter query strings. Use a list to build up the query
    query = ['SELECT tested.* FROM tested, student, exercise WHERE '\
            'tested.student_id=student.id AND tested.exercise_name=exercise.name', ' AND ']

    # Dynaically add each criteria to the query
    for key in student_details:
        value = student_details[key]
        # Check if the value is a number
        if isinstance(value, numbers.Number):
            query.extend(['student.', key, '=', str(value), ' AND '])
        else:
            # Do not use empty strings
            if len(value) == 0:
                continue
            query.extend(['student.', key, '="', value, '"', ' AND '])
    for key in exercise_details:
        value = exercise_details[key]
        if isinstance(value, numbers.Number):
            query.extend(['exercise.', key, '=', str(value), ' AND '])
        else:
            if len(value) == 0:
                continue
            query.extend(['exercise.', key, '="', value, '"', ' AND '])
    # Remove the final extra AND
    query.pop()

    try:
        connection = engine.connect()
        sql = ''.join(query)
        print(sql)
        result = connection.execute(sql)
        connection.close()
        return result
    except Exception as e:
        raise SQLError(repr(e))


# Handle queries involving criteria in 1 table
def querySingleTable(table_name, details):
    # Base query
    query = ['SELECT tested.* FROM tested, {} WHERE '.format(table_name)]
    # Different foreign key checks for the 2 tables
    if table_name == 'student':
        query.append('tested.student_id=student.id AND ')
    else:
        query.append('tested.exercise_name=exercise.name AND ')

    for key in details:
        value = details[key]
        if isinstance(value, numbers.Number):
            query.extend([table_name, '.', key, '=', str(value), ' AND '])
        else:
            if len(value) == 0:
                continue
            query.extend([table_name, '.', key, '="', value, '"', ' AND '])
    query.pop()

    try:
        connection = engine.connect()
        sql = ''.join(query)
        print(sql)
        result = connection.execute(sql)
        connection.close()
        return result
    except Exception as e:
        raise SQLError(repr(e))


# Handle default queries (no criteria)
def queryTested():
    try:
        connection = engine.connect()
        sql = 'SELECT * FROM tested'
        print(sql)
        result = connection.execute(sql)
        connection.close()
        return result
    except Exception as e:
        raise SQLError(repr(e))
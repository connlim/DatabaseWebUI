from flask import Flask, request, session, g, redirect, url_for, abort, render_template, jsonify
from sqlalchemy import create_engine, MetaData, Table
import numbers


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
# Load config and override config from environment variable
app.config.update(
    DEBUG='True',
    MYSQL_DATABASE_HOST='127.0.0.1',
    MYSQL_DATABASE_PORT=3306,
    MYSQL_DATABASE_USER='root',
    MYSQL_DATABASE_DB='pe'
)
#app.config.from_envvar('FLASKR_SETTINGS', silent=True)
engine = create_engine('mysql://root:@localhost/pe', convert_unicode=True)
metadata = MetaData(bind=engine)


@app.route('/')
@app.route('/search', methods=['GET'])
def search():
    return render_template('search.html')


@app.route('/search', methods=['POST'])
def search_post():
    if request.form.get('use_student') and request.form.get('use_exercise'):
        student_details = {'id': request.form.get('student_id'), 'weight': request.form.get('weight'), 
                            'height': request.form.get('height'), 'sex': request.form.get('sex')}
        exercise_details = {'name': request.form.get('exercise_name'), 'type': request.form.get('type'), 
                            'intensity': request.form.get('intensity')}
        result = queryDoubleTables(student_details, exercise_details)
        return render_template('browse.html', title='Search Results', entries=[result], table_names=['tested'])
    elif request.form.get('use_student'):
        student_details = {'id': request.form.get('student_id'), 'weight': request.form.get('weight'), 
                            'height': request.form.get('height'), 'sex': request.form.get('sex')}
        result = querySingleTable('student', student_details)
        return render_template('browse.html', title='Search Results', entries=[result], table_names=['tested'])
    elif request.form.get('use_exercise'):
        exercise_details = {'name': request.form.get('exercise_name'), 'type': request.form.get('type'), 
                            'intensity': request.form.get('intensity')}
        result = querySingleTable('exercise', exercise_details)
        return render_template('browse.html', title='Search Results', entries=[result], table_names=['tested'])
    else:
        result = queryTested()
        return render_template('browse.html', title='All Records (no criteria selected)', entries=[result], table_names=['tested'])
        

@app.route('/browse')
def browse():
    try:
        connection = engine.connect()
        result = []
        table_names = []
        tables = connection.execute('show tables')
        for table_name in tables:
            result.append(connection.execute('SELECT * FROM ' + table_name[0]))
            table_names.append(table_name[0])
        connection.close()
        return render_template('browse.html', title='Browse', entries=result, table_names=table_names)
    except Exception as e:
        raise SQLError(repr(e))
        

@app.errorhandler(SQLError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def queryDoubleTables(student_details, exercise_details):
    query = ['SELECT tested.* FROM tested, student, exercise WHERE '\
            'tested.student_id=student.id AND tested.exercise_name=exercise.name', ' AND ']

    for key in student_details:
        value = student_details[key]
        if isinstance(value, numbers.Number):
            query.extend(['student.', key, '=', str(value), ' AND '])
        else:
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


def querySingleTable(table_name, details):
    query = ['SELECT tested.* FROM tested, {} WHERE '.format(table_name)]
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
from flask import Flask, request, session, g, redirect, url_for, abort, render_template
from sqlalchemy import create_engine, MetaData, Table

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
@app.route('/search')
def index():
    return render_template('search.html')


@app.route('/browse')
def browse():
    connection = engine.connect()
    result = []
    table_names = []
    tables = connection.execute('show tables')
    for table_name in tables:
        result.append(connection.execute('select * from ' + table_name[0]))
        table_names.append(table_name[0])
    connection.close()
    return render_template('browse.html', entries=result, table_names=table_names)


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

from flask import Flask, jsonify, request
import psycopg2
import os
t = os.environ.get('TABLE_NAME')
postgresip = os.environ.get('POSTGRESIP')
port = os.environ.get('POSTGRES_PORT')

con = psycopg2.connect(host=postgresip,
                       port=port,
                       database='postgres',
                       user='postgres',
                       password='postgres')
con.autocommit = True

def CheckIFUserExists(user_id):
    cur = con.cursor()
    cur.execute(f"""
        select * from {t} where id='{user_id}' 
    """)
    if cur.fetchone() is not None:
        return True
    else:
        return False

def CreateTable(tablename):
    cur = con.cursor()
    cur.execute(f"""
    CREATE TABLE  IF NOT EXISTS {tablename} (id SERIAL , username TEXT) 

""")
    cur.close()



CreateTable(t)
app = Flask(__name__)
@app.route('/')
def index():
    return 'HOME PAGE '


@app.route('/api/v1/users', methods=['GET'])
def ListAllUsers():
    cur = con.cursor()
    cur.execute(f"""select * from {t} """)
    return jsonify(cur.fetchall())


@app.route('/api/v1/users', methods=['POST'])
def addUser():
    req = request.get_json()
    if not 'username' in req:
        return 'ERROR: no username found '
    username = req['username']
    cur = con.cursor()
    cur.execute(f""" INSERT INTO {t}( username) VALUES ( '{username}');
""")
    return "user Created "


@app.route('/api/v1/users', methods=['DELETE'])
def DeleteUserById():
    req = request.get_json()
    if not 'id' in req:
        return 'ERROR: no id found ',404
    user_id=req['id']
    if CheckIFUserExists(user_id):
        cur = con.cursor()
        cur.execute(f"""DELETE FROM {t} WHERE id='{user_id}' """)
        return "Deleted"
    else:
        return "user Not Found",404


    return jsonify(cur.fetchall())


@app.route('/api/v1/DeleteAllByName',methods=['DELETE'])
def DeleteUserByUsername():
    req = request.get_json()
    if not 'username' in req :
        return 'ERORE : No user Found'
    user_name=req['username']
    cur = con.cursor()
    cur.execute(f"""DELETE from {t} where username='{user_name}'""")
    return 'Deleted' 


app.run(debug=True,host='0.0.0.0')

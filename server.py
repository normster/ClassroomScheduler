from flask import Flask
from flask import request
from flask import jsonify
import sqlite3
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello world'

@app.route('/class', methods=['GET'])
def test_class():
    conn = sqlite3.connect('locations.db')
    curs = conn.cursor()
    day, timeslot, room, building
    d = request.form['day']
    t = request.form['timeslot']
    r = request.form['room']
    b = request.form['building']
    curs.execute("SELECT * FROM locations WHERE day = d AND timeslot = t AND room = r AND building = b")
    results = curs.fetchall()
    answer = False
    if results:
        answer = True

    d = {'result': answer}
    conn.close()
    return jsonify(**d)

if __name__ == '__main__':
    app.run()

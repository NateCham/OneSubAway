from flask import (Flask, jsonify, render_template, request)
import MySQLdb, MySQLdb.cursors
import import_csv
import json
import time
from contextlib import closing
app = Flask(__name__)

@app.route('/', methods=['GET'])
@app.route('/', defaults={'path': ''})
def root(*args, **kwargs):
    import_csv.read_realtime()
    '''render and init backbone page'''
    return render_template('index.html')

@app.route('/stop/<station_id>')
def get_stops(station_id):
    print('stop/station_id')

    start = time.time()

    db = MySQLdb.connect(host='localhost', user='root', db='nyc_subway2', cursorclass=MySQLdb.cursors.DictCursor)
    with closing(db.cursor()) as cur:
        sql = "SELECT route_id, trip_headsign, direction_id, stop_id, arrival - unix_timestamp() AS train_comes_sec, arrival from stop_time_update stu join trips on stu.trip_id = substring(trips.trip_id, 14, 14) WHERE stop_id IN (SELECT stop_id FROM stops WHERE stop_id = '" + station_id + "' or parent_station = '" + station_id + "') GROUP BY stu.trip_id HAVING train_comes_sec > 0 ORDER BY train_comes_sec ASC LIMIT 5" 
        cur.execute(sql) 

        ret = cur.fetchall()
    db.close()

    elapsed = time.time() - start
    print(elapsed)
    print(sql)

    return jsonify({'query': sql, 'stations': [s for s in ret]})

@app.route('/nearest')
def get_nearest_stops():
    print('nearest')

    start = time.time()

    db = MySQLdb.connect(host='localhost', user='root', db='nyc_subway2', cursorclass=MySQLdb.cursors.DictCursor)
    with closing(db.cursor()) as cur:
        sql = 'call get_closest(' + request.args.get('latitude') + ',' + request.args.get('longitude') + ', 1, 5)'
        cur.execute(sql)
        ret = cur.fetchall()
    db.close()

    elapsed = time.time() - start
    print(elapsed)

    return jsonify({'query': sql, 'nearest': [s for s in ret]})

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')

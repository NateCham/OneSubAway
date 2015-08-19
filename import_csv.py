import pandas
from contextlib import closing
import pprint
import urllib
import MySQLdb
import json
import time
import protobuf_json
from google.transit import gtfs_realtime_pb2
from sqlalchemy import create_engine


csv_file_names = ['agency', 'calendar_dates', 'shapes', 'stop_times', 'transfers', 'calendar', 'routes', 'stops', 'trips']

db_engine = create_engine('mysql://root@localhost/nyc_subway2', pool_size=100, pool_recycle=3600)

pp = pprint.PrettyPrinter(indent=2)

def read_csv():
    # use pandas to import csv to dataframe and export to mysql table
    for c in csv_file_names:
        df = pandas.read_csv('mta_info_files/' + c + '.txt')
        df.to_sql(c, db_engine, if_exists='replace', chunksize=1000)


feed = gtfs_realtime_pb2.FeedMessage()
api_key = "77fdd704a4617f3ffea4e398da8af32e"
feed_ids = ['1', '2']

def make_trip(t, updated):
    trip = {}
    trip['trip_id'] = t.trip_id
    trip['start_date'] = t.start_date
    trip['route_id'] = t.route_id
    trip['updated'] = updated

    return trip

def make_stop_time_update(t, stu, updated):
    stop_time_update = {}
    stop_time_update['trip_id'] = t.trip_id
    if stu.departure:
        stop_time_update['departure'] = stu.departure.time
    if stu.arrival:
        stop_time_update['arrival'] = stu.arrival.time
    stop_time_update['stop_id'] = stu.stop_id
    stop_time_update['updated'] = updated

    return stop_time_update

def make_vehicle(v, updated):
    vehicle = {}
    vehicle['trip_id'] = v.trip.trip_id
    vehicle['curr_stop_seq'] = v.current_stop_sequence
    vehicle['curr_status'] = v.current_status
    vehicle['timestamp'] = v.timestamp
    vehicle['stop_id'] = v.stop_id
    vehicle['updated'] = updated

    return vehicle

def insert_values(values, cursor, table):
    value_tuples = [tuple(v.values()) for v in values]
    columns = ', '.join(values[0].keys())
    placeholders = ", ".join(["%s"] * len(values[0]))

    sql = "INSERT INTO %s(%s) VALUES (%s)" % (table, columns, placeholders)

    cursor.executemany(sql, value_tuples)

def read_realtime():
    print('loading realtime data')
    trips = []
    stop_time_updates = []
    vehicles = []

    for feed_id in feed_ids:
        print('loading feed: ' + feed_id)
        updated = int(time.time())
        response = urllib.urlopen('http://datamine.mta.info/mta_esi.php?key=' + api_key + '&feed_id=' + feed_id)
        feed.ParseFromString(response.read())

        for entity in feed.entity:
            if entity.HasField('trip_update'):
                trips.append(make_trip(entity.trip_update.trip, updated))
                for s in entity.trip_update.stop_time_update:
                    stop_time_updates.append(make_stop_time_update(entity.trip_update.trip, s, updated))

            elif entity.HasField('vehicle'):
                vehicles.append(make_vehicle(entity.vehicle, updated))

            else:
                print(entity)

        db = MySQLdb.connect(host='localhost', user='root', db='nyc_subway2')
        with closing(db.cursor()) as cur:
            insert_values(vehicles, cur, 'vehicle')
            insert_values(stop_time_updates, cur, 'stop_time_update')
            insert_values(trips, cur, 'trip')
            db.commit()
        db.close()
        
read_csv()

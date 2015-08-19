from google.transit import gtfs_realtime_pb2
import urllib

api_key = "77fdd704a4617f3ffea4e398da8af32e"

feed = gtfs_realtime_pb2.FeedMessage()
response = urllib.urlopen('http://datamine.mta.info/mta_esi.php?key=' + api_key + '&feed_id=1')
feed.ParseFromString(response.read())

for entity in feed.entity:
    print(entity)
#if entity.HasField('trip_update'):
#    print(entity.trip_update)


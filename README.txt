Simple Flask + Backbone.JS app to display the subway times for the nearest stations for NYC MTA

Prereqs:
- Flask (pip install Flask)
- Backbone, Underscore, JQuery (referenced from CDN)
- MySQL
- Pandas (pip install pandas)
- protobuf (pip install protobuf)
- Python GTFS-realtime Language Bindings (pip install gtfs-realtime-bindings)
- SQLAlchemy (pip install sqlalchemy)


Steps:
- Init the MySQL Database: $ mysql -uroot < sqlfiles/create_tables.sql
- Add the helper function and procedure: $ mysql -uroot < sqlfiles/helper_functions.sql


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
- Start MySQL server
- Init the MySQL Database: $ mysql -uroot < sqlfiles/create_tables.sql
- Add the helper function and procedure: $ mysql -uroot < sqlfiles/helper_functions.sql
- Import data from text files into the MySQL server: $ python import_csv.py
- Start the webserver: $ python site.py




Hosted:
http://ec2-52-11-54-76.us-west-2.compute.amazonaws.com:5000/


Notes:
- I focused on the backend, but I did use Backbone.JS as the front-end framework to display the data
- Flask is used on the backend to serve the API endpoints to get data from the MySQL database, Backbone hits these endpoints to gather its data. This means the back and front end are completely independent of each other and can be changed if needed. A service oriented architecture was the best choice in my opinion.
- The app is extreeeemly slow. The MySQL queries take an enormous amount of time, so data collection and faster queries would be the focus if I spent more time on this. There are plenty of inefficiencies that I would devote my time to.

use nyc_subway2;

drop table if exists vehicle;
drop table if exists trip;
drop table if exists stop_time_update;

create table if not exists vehicle (
  trip_id varchar(25),
  curr_stop_seq integer,
  curr_status integer,
  timestamp integer,
  stop_id varchar(10),
  updated integer
);

create table if not exists trip (
  trip_id varchar(25),
  start_date date,
  route_id varchar(5),
  updated integer
);

create table if not exists stop_time_update (
  trip_id varchar(25),
  arrival integer,
  departure integer,
  stop_id varchar(10),
  schedule_relationship enum('SCHEDULED', 'SKIPPED', 'NO_DATA'),
  updated integer
);

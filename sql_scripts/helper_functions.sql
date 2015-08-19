use nyc_subway2;

DROP FUNCTION IF EXISTS DISTANCE;
DELIMITER $$
CREATE FUNCTION DISTANCE( lat1 DOUBLE, lon1 DOUBLE, lat2 DOUBLE, lon2 DOUBLE)
RETURNS DOUBLE
BEGIN
  DECLARE dist, latDist, lonDist, a, c, r DOUBLE;
  
  -- earth's radius
  SET r = 3959;
  
  -- Haversine formula <http://en.wikipedia.org/wiki/Haversine_formula>
  SET latDist = RADIANS( lat2 - lat1 );
  SET lonDist = RADIANS( lon2 - lon1 );
  SET a = POW( SIN( latDist/2 ), 2 ) + COS( RADIANS( lat1 ) ) * COS( RADIANS( lat2 ) ) * POW( SIN( lonDist / 2 ), 2 );
  SET c = 2 * ATAN2( SQRT( a ), SQRT( 1 - a ) );
  SET dist = r * c;  
  
  RETURN dist;
END$$
DELIMITER ;


DROP PROCEDURE IF EXISTS get_closest;

DELIMITER $$
CREATE PROCEDURE get_closest(loc_lat DOUBLE, loc_lon DOUBLE, loc_type INTEGER, limit_quan INTEGER)
BEGIN
  SELECT stop_id, stop_name, stop_lat, stop_lon, DISTANCE(loc_lat, loc_lon, stop_lat, stop_lon) as dist_miles
  FROM (SELECT stop_id, stop_name, stop_lat, stop_lon FROM stops JOIN (SELECT DISTINCT parent_station FROM stops 
  WHERE stop_id IN (SELECT DISTINCT stop_id FROM stop_time_update)) a ON stops.stop_id = a.parent_station) stp 
  ORDER BY dist_miles ASC
  LIMIT limit_quan;
END$$
DELIMITER ;


use nyc_subway2;

/* select the distances between lat/lon given and all parent stations */
/* http://postcodepal.com/?page=mysql-query */
/* 3961 is the earth's radius in miles near NYC */
/* location_type = 1 is the main stations, 0 is the sub-stations */
DROP PROCEDURE IF EXISTS get_closest;

DELIMITER $$
CREATE PROCEDURE get_closest(loc_lat DECIMAL(8,6), loc_lon DECIMAL(8,6), loc_type INTEGER)
BEGIN
  SELECT stop_id, stop_name, stop_lat, stop_lon, ACOS(SIN(RADIANS(loc_lat)) * SIN(RADIANS(stop_lat)) + 
              COS(RADIANS(loc_lat)) * COS(RADIANS(stop_lat)) * 
              COS(RADIANS(stop_lon) - RADIANS(loc_lon))) * 3961 AS distance
  FROM stops 
  WHERE location_type = loc_type 
  ORDER BY distance ASC;
END$$
DELIMITER ;


CALL get_closest(40.7354637,-73.991226,1);

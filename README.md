# Nextbike Berlin Trip Dataset
This repository is dedicated to experimenting with nextbike public API maps, and eventually, hoping to create a dataset containing station information, 
trip information of bikes, and also more generally total bikes being used in city of Berlin.

#### Update: 24/04/2025

- created a proxy requester to avoid being blocked (to be safe)
- created an ETL pipeline for the initial extraction and upload it into separate csv files
- tested ETL for 10 minutes
- worked and made a progress on second layer of ET extraction and transformation, to get trips and their duration from bikes data.
- Need to do:
    - finish second layer of transformation to minimize make data compact to be able to save it locally
    - clean stations data (remove duplicates, figure out spots that are time-stationary, only add when bike is a spot)
    - index bikes and stations data, so that, joining them would be possible in database
    - for stationary places that are stations, remove date as we do not know when they appeared
    - for new standalone bike spots, possibly in future, temporary_stations_table could be constructed

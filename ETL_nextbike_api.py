
import pandas as pd
import datetime
from requester import request_data
import os

def extract(url):
    timestamp = datetime.datetime.now()
    response = request_data(url)
    return timestamp, response


def get_city_specs(data, time):

    country = data.get('countries')[0]
    city = country.get('cities')[0]
    city_dict = {
        'datetime'          : time,
        'city_id'           : city.get('uid'),
        'city_name'         : city.get('name'),
        'country'           : country.get('country'),
        'country_name'      : country.get('country_name'),
        'timezone'          : country.get('timezone'),
        'latitude'          : country.get('lat'),
        'longitute'         : country.get('lng'),
        'booked_bikes'      : country.get('booked_bikes'),
        'set_point_bikes'   : country.get('set_point_bikes'),
        'available_bikes'   : country.get('available_bikes'),
        'num_places'        : city.get('num_places'),
    }
    return pd.json_normalize(city_dict)

def get_bikes_stations(data, time):
    places = data.get('countries')[0].get('cities')[0].get('places')
    city = data.get('countries')[0].get('cities')[0]

    bikes = []
    stations = []

    for place in places:

        if place.get('bikes') > 0:
            for bike in place.get('bike_list'):
                bike_dic = {
                    'date'          : time,
                    'bike_id'       : bike.get('number'),
                    'bike_lat'      : place.get('lat'),
                    'bike_lng'      : place.get('lng'),
                    'bike_type'     : bike.get('bike_type'),
                    'active'        : bike.get('active'),
                    'state'         : bike.get('state'),
                    'electric_lock' : bike.get('electric_lock'),
                    'boardcomputer' : bike.get('boardcomputer'),
                    'is_standalone' : place.get('bike'),
                    'place_uid'     : place.get('uid'),
                    'place_number'  : place.get('number'),
                    'city_id'       : city.get('uid'),
                    'city_name'     : city.get('name')
                }
                bikes.append(bike_dic)

        if place.get('spot'):
            station_dic = {
                'date'                      : time,
                'place_uid'                 : place.get('uid'),
                'place_lat'                 : place.get('lat'),
                'place_lng'                 : place.get('lng'),
                'place_name'                : place.get('name'),
                'place_number'              : place.get('number'),
                'place_type'                : place.get('place_type'),
                'station_booked_bikes'      : place.get("booked_bikes"),
                'num_bikes'                 : place.get("bikes"),
                'bikes_available_to_rent'   : place.get('bikes_available_to_rent'),
                'bike_racks'                : place.get('bike_racks'),
                'free racks'                : place.get('free_racks'),
                'special_racks'             : place.get('special_racks'),
                'free_special_racks'        : place.get('free_special_racks'),
                'terminal_type'             : place.get('terminal_type'),
                'rack_locks'                : place.get('rack_locks'),
                'city_id'                   : city.get('uid'),
                'city_name'                 : city.get('name')
            }
            stations.append(station_dic)

    return pd.json_normalize(bikes), pd.json_normalize(stations)


def transform_response(response, timestamp):

    data = response.json()
    city_info = get_city_specs(data=data, time=timestamp)
    bikes_table, stations_table = get_bikes_stations(data=data, time=timestamp)

    return city_info, bikes_table, stations_table


def load_tables(city_info, bikes_table, stations_table, folder='daily_temp_data'):
    path = folder
    city_path = path + '/city_info.csv'
    bikes_path = path + '/bikes_table.csv'
    stations_path = path + '/stations_table.csv'

    city_info.to_csv(city_path, mode='a', header=not os.path.exists(city_path))
    bikes_table.to_csv(bikes_path, mode='a', header=not os.path.exists(bikes_path))
    stations_table.to_csv(stations_path, mode='a', header=not os.path.exists(stations_path))




def main():

    import time
    for i in range(10):
        url = 'https://api.nextbike.net/maps/nextbike-live.json?city=362'

        # extract response from nextbike API
        timestamp, response = extract(url)

        # transform response into 3 tables consisting of snapshots of bikes, stations data and city info
        city_info, bikes_table, stations_table = transform_response(response, timestamp)

        # load tables into separate csv files
        load_tables(city_info, bikes_table, stations_table)

        print("Loading complete {:d} out of 10".format(i+1))

        time.sleep(60)



if __name__ == "__main__":
    main()

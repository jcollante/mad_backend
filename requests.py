import json
from main import db, pd, gpd
from datetime import datetime, timedelta
from shapely.geometry import Point, Polygon
from shapely import wkt
from geopandas import GeoDataFrame

db_a = gpd.GeoDataFrame(
    columns=['id', 'geometry'], geometry='geometry', crs='EPSG:4326')


def parse_df(df):
    result = df.to_json(orient="records")
    parsed = json.loads(result)


def getVesselById(id: int):
    result = db[db["MMSI"] == id].head(1)
    result = pd.DataFrame(result.drop(columns='geometry'))
    return result.to_json()


def getVessels():
    result = db.head(10)
    result = pd.DataFrame(result.drop(columns='geometry'))
    return result.to_json(orient="records")


def getVesselPathById(id: int, timeframe_min: int, current_time: str):
    result = db[db["MMSI"] == str(id)]
    # convert time of analysis from str to datetime
    current_time_dt = datetime.strptime(
        current_time,        '%Y-%m-%dT%H:%M:%S')
    # substract timeframe in minutes from the time
    time_before_dt = current_time_dt - timedelta(minutes=timeframe_min)
    # return dataset with before <= timeframe <= currenttime
    result = result[(time_before_dt < result['time']) &
                    (result['time'] < current_time_dt)]

    result = result.sort_values(
        'time')[['BaseDateTime', 'COG', 'SOG', 'Heading', 'LAT', 'LON']]
    result = pd.DataFrame(result)
    return result.to_json(orient="records")


def getVesselsInElapsedTime(timeframe_min: int, current_time: str):
    global db_a
    result = db
    if timeframe_min > 0:
        # convert time of analysis from str to datetime
        current_time_dt = datetime.strptime(current_time, '%Y-%m-%dT%H:%M:%S')
        # substract timeframe in minutes from the time
        time_before_dt = current_time_dt - timedelta(minutes=timeframe_min)
        # return dataset with before <= timeframe <= currenttime
        result = db[(time_before_dt < db['time']) &
                    (db['time'] < current_time_dt)]

    # If timeframe_min is negative or 0, then return all boats and their positions
    result = result.sort_values('time').groupby('MMSI').tail(1)
    result['hasAnomaly'] = False
    result['AISLost'] = False

    row = result[result['MMSI'] == "477624800"]

    polygons_contains = gpd.sjoin(
        db_a, result, how='inner', predicate='contains')
    print("\n\n")
    print("POLYGONS--------------------------------------------------\n")
    print(polygons_contains['MMSI'])
    print("\n")

    result = result.merge(
        polygons_contains[['MMSI', 'id']], on='MMSI', how='left')
    result.loc[result['id'].notnull(), 'hasAnomaly'] = True

    result = pd.DataFrame(result.drop(columns='geometry'))
    return result.to_json(orient="records")


def getAllVesselsInElapsedTime(timeframe_min: int, current_time: str):
    global db_a
    result = db
    if timeframe_min > 0:
        # convert time of analysis from str to datetime
        current_time_dt = datetime.strptime(current_time, '%Y-%m-%dT%H:%M:%S')
        # substract timeframe in minutes from the time
        time_before_dt = current_time_dt - timedelta(minutes=timeframe_min)
        # return dataset with timeVessel <= currenttime
        result = db[(db['time'] < current_time_dt)]

    # If timeframe_min is negative or 0, then return all boats and their positions
    result = result.sort_values('time').groupby('MMSI').tail(1)
    result['hasAnomaly'] = False
    result['AISLost'] = False

    polygons_contains = gpd.sjoin(
        db_a, result, how='inner', predicate='contains')

    result = result.merge(
        polygons_contains[['MMSI', 'id']], on='MMSI', how='left')
    result.loc[result['id'].notnull(), 'hasAnomaly'] = True

    result['current_time'] = pd.to_datetime(current_time_dt)
    result['allowed_time'] = pd.to_datetime(result['time'])
    result['time_diff'] = (result['current_time'] -
                           result['allowed_time']) / pd.Timedelta(minutes=1)
    result.loc[((result['current_time'] - result['allowed_time']) / pd.Timedelta(minutes=1)) >= 30,
               'AISLost'] = True

    result = pd.DataFrame(result.drop(
        columns=['geometry', 'current_time', 'allowed_time', 'time_diff']))
    return result.to_json(orient="records")


def uploadAreaJson(jsonArea):
    global db_a
    db_a = gpd.GeoDataFrame(
        columns=['id', 'geometry'], geometry='geometry', crs='EPSG:4326')
    if not jsonArea:
        return

    for areas in jsonArea:
        id = ''
        for k, v in areas.items():

            if k == "id":
                id = v
            if k == "latlngs":
                lon_lat_list = list()
                for element in v:
                    lon_lat_list.append(list(element.values()))

                polygon_geom = Polygon(lon_lat_list)

                geo_row = gpd.GeoDataFrame(
                    {'id': id, 'geometry': [polygon_geom]}, crs="EPSG:4326", geometry='geometry')
                db_a = db_a.append(geo_row, ignore_index=True)

    print(db_a)


# def getVesselsInElapsedTime(timeframe_min: int, current_time: str):
#     result = db

#     if timeframe_min > 0:
#         # convert time of analysis from str to datetime
#         current_time_dt = datetime.strptime(current_time, '%Y-%m-%dT%H:%M:%S')
#         # substract timeframe in minutes from the time
#         time_before_dt = current_time_dt - timedelta(minutes=timeframe_min)
#         # return dataset with before <= timeframe <= currenttime
#         result = db[(time_before_dt < db['time']) &
#                     (db['time'] < current_time_dt)]

#     # If timeframe_min is negative or 0, then return all boats and their positions
#     result = result.sort_values('time').groupby('MMSI').tail(1)
#     result['hasAnomaly'] = False
#     return result.to_json(orient="records")

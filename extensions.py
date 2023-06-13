import pandas as pd
import os
from config import _config
import geopandas as gpd
from geopandas import GeoDataFrame
from shapely.geometry import Point

base_dir = os.path.abspath(os.getcwd())

c = getattr(_config, 'default', 'default')
db = getattr(c, 'DATABASE', 'pandas')
db_a = gpd.GeoDataFrame(
    columns=['id', 'geometry'], geometry='geometry', crs='EPSG:4326')
if db == 'pandas':
    print(base_dir+'/dk_sample.csv')
    # db = pd.read_csv(base_dir+'/AIS_2022_03_13.csv')
    # db = pd.read_csv(base_dir+'/data_for_ef_time.csv')

    # db = gpd.read_file(base_dir+'/data_for_ef_time.csv', driver="CSV",
    #                    X_POSSIBLE_NAMES="LAT", Y_POSSIBLE_NAMES="LON")
    db = gpd.read_file(base_dir+'/deutschland.csv', driver="CSV",
                       X_POSSIBLE_NAMES="LAT", Y_POSSIBLE_NAMES="LON")
    db.crs = 'epsg:4326'
    db['time'] = pd.to_datetime(db['BaseDateTime'], format='%Y-%m-%dT%H:%M:%S')


if db is None:
    db = g._database = sqlite3.connect(DATABASE)

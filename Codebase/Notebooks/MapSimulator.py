import pandas as pd
import numpy as np
import json
from sklearn.neighbors import KNeighborsRegressor
from shapely.geometry import Point
import geopandas as gpd

#Variable Lists

TurtleDataSet_Raw = 'turtle_data.csv' 
Predicted_TurtleDS = 'predicted_turtle_data.csv'
TurtleMetadata = 'turtle_metadata.json' 
Lat_Long_KNN = 5     
MaxDistCovered = 500  
NeighborsForAccuracy = 10        
StartDate_Output = '2024-01-01'
EndDate_Output = '2024-12-31'


MapTemplate = 'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_land.geojson'

def prepare_turtle_data():
    try:
        output_start = pd.to_datetime(StartDate_Output)
        output_end = pd.to_datetime(EndDate_Output)

        print(f"Loading raw data from '{TurtleDataSet_Raw}'...")
        df = pd.read_csv(TurtleDataSet_Raw)
        
        df.columns = df.columns.str.lower().str.replace('[^a-z0-9]', '', regex=True)
 
        lat_col = next((col for col in ['lat', 'latitude'] if col in df.columns), None)
        long_col = next((col for col in ['long', 'longitude'] if col in df.columns), None)
        day_col = next((col for col in ['day', 'd'] if col in df.columns), None)
        month_col = next((col for col in ['month', 'm'] if col in df.columns), None)
        year_col = next((col for col in ['year', 'y'] if col in df.columns), None)
        cols_to_check = [lat_col, long_col, day_col, month_col, year_col]
        
        if not all(cols_to_check):
            print("Error: Could not find all required columns (e.g., lat, long, day, month, year).")
            return
        df_cleaned = df.dropna(subset=cols_to_check).copy()
       
        date_cols_map = {year_col: 'year', month_col: 'month', day_col: 'day'}
        df_cleaned['date'] = pd.to_datetime(df_cleaned[[year_col, month_col, day_col]].rename(columns=date_cols_map), errors='coerce')
        df_cleaned.dropna(subset=['date'], inplace=True)
        
        df_cleaned['year'] = df_cleaned['date'].dt.year
        df_cleaned['day_of_year'] = df_cleaned['date'].dt.dayofyear 

        df_cleaned['latitude'] = df_cleaned[lat_col]
        df_cleaned['longitude'] = df_cleaned[long_col]
        df_train_all = df_cleaned.copy() 

        
        X_train = df_train_all[['day_of_year', 'year']]
        Y_lat_train = df_train_all['latitude']
        Y_lon_train = df_train_all['longitude']

        knn_lat = KNeighborsRegressor(n_neighbors=Lat_Long_KNN)
        knn_lat.fit(X_train, Y_lat_train)
        knn_lon = KNeighborsRegressor(n_neighbors=Lat_Long_KNN)
        knn_lon.fit(X_train, Y_lon_train)

        
        date_range = pd.date_range(start=output_start, end=output_end, freq='D')
        
        trend_features = []
        for date_obj in date_range:
            day_of_year = date_obj.dayofyear
            year = date_obj.year
            time_idx = (date_obj - output_start).days 
            trend_features.append([day_of_year, year, time_idx]) 

        df_trend = pd.DataFrame(trend_features, columns=['day_of_year', 'year', 'time_index'])
        
        X_trend = df_trend[['day_of_year', 'year']]
        df_trend['latitude'] = knn_lat.predict(X_trend)
        df_trend['longitude'] = knn_lon.predict(X_trend)
        
        max_time_index = df_trend['time_index'].max()
        
        knn_geo_dist = KNeighborsRegressor(n_neighbors=NeighborsForAccuracy, metric='haversine')
        X_geo_train = np.radians(df_train_all[['latitude', 'longitude']].values)
        knn_geo_dist.fit(X_geo_train, np.zeros(len(X_geo_train))) 

        X_geo_trend = np.radians(df_trend[['latitude', 'longitude']].values)
        distances, _ = knn_geo_dist.kneighbors(X_geo_trend)
        
        mean_dist_rad = distances.mean(axis=1) 
        
        mean_dist_km = mean_dist_rad * 6371 

        df_trend['mean_dist_km'] = mean_dist_km
        
        df_trend_filtered = df_trend[df_trend['mean_dist_km'] <= MaxDistCovered].copy()

        print("Filtering trend points based on geography (removing land points)...")
        
        df_trend_final = df_trend_filtered.copy() 
        
        try:
        
            land = gpd.read_file(MapTemplate)
            geometry = [Point(xy) for xy in zip(df_trend_filtered['longitude'], df_trend_filtered['latitude'])]
            gdf_trend = gpd.GeoDataFrame(df_trend_filtered, geometry=geometry, crs="EPSG:4326")

            points_on_land = gpd.sjoin(gdf_trend, land, predicate='intersects', how='inner')
            land_indices = points_on_land.index.tolist()
            
            df_trend_final = df_trend_filtered.drop(land_indices).copy()

        except Exception as e:
            df_trend_final = df_trend_filtered.copy()


        df_train_output = df_train_all[
            (df_train_all['date'] >= output_start) & 
            (df_train_all['date'] <= output_end)
        ].copy()
        
        df_train_output['time_index'] = (df_train_output['date'] - output_start).dt.days
        
    
        df_trend_final['is_trend'] = True
        df_trend_final['time_index'] = df_trend_final['time_index'].astype(int) 
        
        df_train_output['is_trend'] = False 
        df_train_output['time_index'] = df_train_output['time_index'].astype(int) 

        df_train_export = df_train_output[['latitude', 'longitude', 'time_index', 'is_trend']].copy()
        df_trend_export = df_trend_final[['latitude', 'longitude', 'time_index', 'is_trend']].copy()

        df_combined = pd.concat([df_train_export, df_trend_export], ignore_index=True)
        
        df_combined.to_csv(Predicted_TurtleDS, index=False)
        
        metadata = {
            'minDate': output_start.strftime('%Y-%m-%d'),
            'maxTimeIndex': max_time_index
        }
        with open(TurtleMetadata, 'w') as f:
            json.dump(metadata, f, indent=4)
        
        
    except FileNotFoundError:
        print(f"Error: Raw file '{TurtleDataSet_Raw}' not found.")
    except ImportError as ie:
        print(f"Error: Required library not found. Please install: {ie}")
        print("Required libraries: pandas, numpy, scikit-learn, shapely, geopandas.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    prepare_turtle_data()

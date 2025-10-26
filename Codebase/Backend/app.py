from flask import Flask, jsonify
from flask_socketio import SocketIO
from sgp4.api import Satrec, jday
from datetime import datetime, timezone
from skyfield.api import wgs84, load
from skyfield.constants import AU_KM
from skyfield.positionlib import Geocentric
from utils.city_lookup import load_cities, get_nearest_city
import json

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

with open('data/satellites.json') as satelliteData:
    satellites_raw = json.load(satelliteData)

satellites = []
for sat in satellites_raw:
    srec = Satrec.twoline2rv(sat['tle1'], sat['tle2'])
    satellites.append({
        'name': sat['name'],
        'norad_id': sat.get('norad_id'),
        'tle1': sat['tle1'],
        'tle2': sat['tle2'],
        'satrec': srec,
        'operator': sat.get('operator'),
        'launch_date': sat.get('launch_date'),
        'mission': sat.get('mission'),
        'status': sat.get('status'),
    })

ts = load.timescale()

load_cities("data/cities500.txt")

def calculate_positions():
    now = datetime.now(timezone.utc)
    jd, fr = jday(
        now.year, now.month, now.day,
        now.hour, now.minute,
        now.second + now.microsecond * 1e-6
    )
    t = ts.from_datetime(now)

    results = []
    for sat in satellites:
        s = sat['satrec']
        e, r, v = s.sgp4(jd, fr)
        if e == 0:
            speed_kmps = (v[0] ** 2 + v[1] ** 2 + v[2] ** 2) ** 0.5

            x_au, y_au, z_au = [coord / AU_KM for coord in r]
            position = Geocentric([x_au, y_au, z_au], t=t, center=399, target=399)
            subpoint = wgs84.subpoint(position)
            lat = subpoint.latitude.degrees
            lon = subpoint.longitude.degrees
            alt = subpoint.elevation.km

            city_info = get_nearest_city(lat, lon)

            results.append({
                'timestamp': now.isoformat(),
                'norad_id': sat['norad_id'],
                'name': sat['name'],

                'tle1': sat['tle1'],
                'tle2': sat['tle2'],

                'eci': {'x': r[0], 'y': r[1], 'z': r[2]},
                'geodetic': {'lat': lat, 'lon': lon, 'alt': alt},

                'nearby_city': (
                    f"{city_info['name']}, {city_info['country']}"
                    if city_info else "No major city nearby"
                ),
                'speed_kmps': speed_kmps,

                'operator': sat.get('operator'),
                'launch_date': sat.get('launch_date'),
                'mission': sat.get('mission'),
                'status': sat.get('status'),
            })
    return results

def broadcast_positions():
    while True:
        data = calculate_positions()
        socketio.emit('positions', data)
        socketio.sleep(3)

@app.route('/api/satellites')
def get_satellites():
    satellite_list = [
        {
            'name': sat['name'],
            'norad_id': sat['norad_id'],
            'tle1': sat['tle1'],
            'tle2': sat['tle2'],
            'operator': sat.get('operator'),
            'launch_date': sat.get('launch_date'),
            'mission': sat.get('mission'),
            'status': sat.get('status'),
        }
        for sat in satellites
    ]
    return jsonify(satellite_list)

@socketio.on('connect')
def on_connect():
    print("Frontend connected to WebSocket")

socketio.start_background_task(broadcast_positions)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000, debug=True, use_reloader=False)
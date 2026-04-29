from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/weather', methods=['GET'])
def get_weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({'error': 'Missing lat or lon parameters'}), 400

    url = f'https://api.open-meteo.com/v1/weather?latitude={lat}&longitude={lon}&current_weather=true'
                                                                                          
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch data from Open-Meteo API'}), 500

    data = response.json()
    wind_speed_kmh = data['current_weather']['windspeed']
    wind_direction_deg = data['current_weather']['winddirection']

    # Convert km/h to mph
    wind_speed_mph = wind_speed_kmh * 0.621371

    # Convert wind direction in degrees to compass text
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    index = round(wind_direction_deg / 45) % 8
    wind_direction_compass = directions[index]

    # Create response JSON
    response_data = {
        'windspeed_mph': wind_speed_mph,
        'winddirection_compass': wind_direction_compass
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
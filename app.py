from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/wind', methods=['GET'])
def get_wind():
    lat = request.args.get('lat')
    lng = request.args.get('lng')

    if not lat or not lng:
        return jsonify({'error': 'Missing lat or lng'}), 400

    url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lng}&current=wind_speed_10m,wind_direction_10m,wind_gusts_10m'
    
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch weather data'}), 500

    data = response.json()
    current = data.get('current', {})
    
    wind_speed_kmh = current.get('wind_speed_10m', 0)
    wind_direction_deg = current.get('wind_direction_10m', 0)
    wind_gusts_kmh = current.get('wind_gusts_10m', 0)

    # Convert km/h to mph
    wind_speed_mph = round(wind_speed_kmh * 0.621371, 1)
    wind_gusts_mph = round(wind_gusts_kmh * 0.621371, 1)

    # Convert degrees to compass direction
    directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    index = round(wind_direction_deg / 22.5) % 16
    wind_direction_text = directions[index]

    return jsonify({
        'speed': wind_speed_mph,
        'direction': round(wind_direction_deg),
        'direction_text': wind_direction_text,
        'gusts': wind_gusts_mph
    })

if __name__ == '__main__':
    app.run(debug=True)

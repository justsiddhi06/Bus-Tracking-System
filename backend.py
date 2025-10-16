# app.py
from flask import Flask, jsonify, render_template, request
import geocoder
import folium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time

app = Flask(__name__)

'''@app.route('/')
def Login():
    
    return render_template('login.html')'''

@app.route('/')
def index():
    #show_on_map()  # Call the function to display the map
    return render_template('index.html')

@app.route('/process', methods=['POST']) 
def process(): 
    data = request.get_json()
    # Process the received data, for example, you can store it in a database
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    # Perform any processing you need to do with the received location data
    print(latitude,longitude)
    # Return a response to the client
    return show_on_map(latitude, longitude),jsonify({'result': 'Location received and processed successfully'})
   # return jsonify({'result': 'Location received and processed successfully'})

@app.route('/show_on_map')
def show_on_map(latitude, longitude):
    map_center = [latitude, longitude]
    my_map = folium.Map(location=map_center, zoom_start=15)
    folium.Marker(location=map_center, popup='Location').add_to(my_map)

    # Add another fixed location (example coordinates)
    fixed_location1 = [26.7796, 75.8771]  # Example coordinates (Los Angeles)
    folium.Marker(location=fixed_location1, popup='Fixed Location1').add_to(my_map)

    # Connect both points with a path
    path = folium.PolyLine(locations=[map_center, fixed_location1], color='blue')
    my_map.add_child(path)

    my_map.save('templates/map.html')  # Use a relative path
    return render_template('map.html')

@app.route('/show_map')
def show_map():
    # Logic to generate map data
    # For example, you can use Folium to generate the map
    # Return the map template
    return render_template('map.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

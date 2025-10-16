from flask import Flask, render_template, request, jsonify
import pymysql.cursors

# Initialize Flask application
app = Flask(__name__)

# MySQL connection configuration
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='Karan1234@',
    database='BusDetails',
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/')
def bus_deatils():
    #show_on_map()  # Call the function to display the map
    return render_template('inputbusdetails.html')

# Endpoint to fetch bus details
@app.route('/bus_details', methods=['GET'])
def get_bus_details():
    try:
        with connection.cursor() as cursor:
            # Fetch bus details from the database
            sql = "SELECT * FROM BusInfo"
            cursor.execute(sql)
            bus_details = cursor.fetchall()
            return jsonify(bus_details)
    except Exception as e:
        return jsonify({'error': str(e)})

# Endpoint to add bus details
@app.route('/add_bus', methods=['POST'])
def add_bus():
    try:
        bus_no = int(request.form['bus_no'])
        driver_name = request.form['driver_name']
        driver_contact = int(request.form['driver_contact'])
        route = request.form['route']
        
        with connection.cursor() as cursor:
            # Insert bus details into the database
            sql = "INSERT INTO BusInfo (bus_no, driver_name, driver_contact, route) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (bus_no, driver_name, driver_contact, route))
            connection.commit()
        
        return 'Bus details added successfully!'
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/show_busdetails')
def show_busdetails():
    return render_template('bus_details.html')

if __name__ == '__main__':
    app.run(debug=True)

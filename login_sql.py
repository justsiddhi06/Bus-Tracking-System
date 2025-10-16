from flask import Flask, request, render_template, redirect, url_for, session
import pymysql

app = Flask(__name__)
app.secret_key = '46c3faab273b848029ed1d416843de4c'

# MySQL Connection Configuration
db = None

def connect_to_database():
    global db
    db = pymysql.connect(host="localhost", user="root", password="Karan1234@", database="busdetails")

# Function to get database cursor
def get_cursor():
    global db
    try:
        if db is None:
            connect_to_database()
        return db.cursor()
    except pymysql.MySQLError as e:
        # Handle connection errors, reconnect, or log the error
        print("MySQL Connection Error:", e)
        raise

@app.route('/')
def test():
    return render_template('signup.html')

@app.route('/store_location', methods=['POST'])
def store_location():
    try:
        data = request.json
        bus_no = data['busNumber']
        latitude = data['latitude']
        longitude = data['longitude']
        print(bus_no, latitude, longitude)

        cursor = get_cursor()

        # Check if data already exists for the given bus number
        cursor.execute("SELECT * FROM businfo WHERE bus_no = %s", (bus_no,))
        existing_data = cursor.fetchone()

        if existing_data:
            # If data exists for the bus number, update it
            sql = "UPDATE businfo SET latitude = %s, longitude = %s WHERE bus_no = %s"
            cursor.execute(sql, (latitude, longitude, bus_no))
            db.commit()
            return "Location updated successfully!"
        else:
            # If data doesn't exist for the bus number, insert a new row
            sql = "INSERT INTO businfo (bus_no, latitude, longitude) VALUES (%s, %s, %s)"
            cursor.execute(sql, (bus_no, latitude, longitude))
            db.commit()
            return "Location stored successfully!"
    except pymysql.MySQLError as e:
        db.rollback()
        return str(e)

@app.route('/signup_driver', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return render_template('signup.html', error='Passwords do not match')

        cursor = get_cursor()
        cursor.execute("SELECT * FROM drivers WHERE username = %s", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            return render_template('signup.html', error='Username already exists')

        # Store the original password in the database
        cursor.execute("INSERT INTO drivers (username, password) VALUES (%s, %s)", (username, password))
        db.commit()

        session['username'] = username
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login_driver', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = get_cursor()
        cursor.execute("SELECT * FROM drivers WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        if user:
            session['username'] = username

            # Fetch the bus number associated with the logged-in driver
            cursor.execute("SELECT bus_no FROM businfo WHERE driver_name = %s", (username,))
            bus_no = cursor.fetchone()[0]

            # Pass busNumber to the template
            return render_template("BusLocationupdate.html", busNumber=bus_no)
        else:
            return redirect(url_for('signup'))  # Redirect to signup page if not found

    return render_template('login.html')

@app.route('/open_signup')
def open_signup():
    return render_template('signup.html')

@app.route('/show_login')
def show_login():
    # Logic to generate map data
    # For example, you can use Folium to generate the map
    
    # Retrieve the bus number dynamically from Flask
    cursor = get_cursor()
    cursor.execute("SELECT bus_no FROM businfo WHERE driver_name = %s", (session['username'],))
    bus_no = cursor.fetchone()[0]

    # Render the template and pass the bus number
    return render_template('login.html', busNumber=bus_no)

if __name__ == '__main__':
    app.run(debug=True)

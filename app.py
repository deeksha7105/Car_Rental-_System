from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change to a secure random key in production

# Database connection setup
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_mysql_password",
    database="car_rental_db"
)
cursor = db.cursor(dictionary=True)

#Home page
@app.route('/')
def home():
    return render_template('home.html')


# Login page 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['email'] = user['email']
            flash('Login successful!', 'success')

            # Redirect based on role
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user['role'] == 'client':
                return redirect(url_for('client_dashboard'))
            elif user['role'] == 'employee':
                return redirect(url_for('employee_dashboard'))
            else:
                return redirect(url_for('customer_dashboard'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    return "Admin Dashboard"

@app.route('/client/dashboard')
def client_dashboard():
    return "Client Dashboard"

@app.route('/employee/dashboard')
def employee_dashboard():
    return "Employee Dashboard"

@app.route('/customer/dashboard')
def customer_dashboard():
    return "Customer Dashboard"

if __name__ == '__main__':
    app.run(debug=True)

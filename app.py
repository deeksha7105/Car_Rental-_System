from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ---------------- Database Connection ----------------
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='your_db_user',
        password='your_db_password',
        database='car_rental_db'
    )

# ---------------- Home Page ----------------
@app.route('/')
def home():
    return render_template('home.html')

# ---------------- Register Page (Customer Only) ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['cust_name']
        address = request.form['cust_address']
        contact = request.form['cust_contact']
        licence = request.form['cust_licence']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return redirect(url_for('register'))

        hashed_pw = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # 1. Insert into CUSTOMER
            cursor.execute("""
                INSERT INTO CUSTOMER (cust_name, cust_address, cust_contact, cust_licence)
                VALUES (%s, %s, %s, %s)
            """, (name, address, contact, licence))
            cust_id = cursor.lastrowid

            # 2. Insert into USERS
            cursor.execute("""
                INSERT INTO USERS (Email, Password, Role, RefID)
                VALUES (%s, %s, 'customer', %s)
            """, (email, hashed_pw, cust_id))

            conn.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))

        except mysql.connector.IntegrityError:
            flash("Email already exists!", "danger")
            return redirect(url_for('register'))

        finally:
            cursor.close()
            conn.close()

    return render_template('register.html')

# ---------------- Login Page (All Roles) ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM USERS WHERE Email = %s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user['Password'], password):
            session['user_id'] = user['UserID']
            session['email'] = user['Email']
            session['role'] = user['Role']
            session['ref_id'] = user['RefID']
            flash(f"Welcome {user['Role'].capitalize()}!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid email or password", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')

# ---------------- Logout ----------------
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully", "info")
    return redirect(url_for('login'))

# ---------------- Run ----------------
if __name__ == '__main__':
    app.run(debug=True)

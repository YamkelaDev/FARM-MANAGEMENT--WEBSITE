from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'Sister_bethina'  

# Database connection
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost', 
        port=3307,         
        user='YUM',  
        password='Yum%24082.ksi',  
        database='KSIMS'
    )
    return connection
    # Define the home route
@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
                flash('Login failed. Please check your username and password.', 'danger')
    return render_template('login.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/add_farmer', methods=['GET', 'POST'])
def add_farmer():
    if request.method == 'POST':
        unique_code = request.form['unique_code']
        name = request.form['name']
        surname = request.form['surname']
        id_number = request.form['id_number']
        bank_details = request.form['bank_details']
        contact_number = request.form['contact_number']
        address = request.form['address']
        household = request.form['household']
        location = request.form['location']
        land_size = request.form['land_size']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
              INSERT INTO Farmers (UniqueCode, Name, Surname, IDNumber, BankDetails, ContactNumber, Address, Household, Location, LandSize)
              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (unique_code, name, surname, id_number, bank_details, contact_number, address, household, location, land_size))
            conn.commit()
            flash('Farmer added successfully!', 'success')
        except Exception as e:
             conn.rollback()
             flash('Error adding farmer. Please try again.', 'danger')
        finally:
             conn.close()
        
        return redirect(url_for('dashboard'))
    return render_template('add_farmer.html')

UPLOAD_FOLDER = 'documents' 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload_file/<string:main_folder>/<string:subfolder>', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded', 'success')
            return redirect(url_for('dashboard'))
    return render_template('upload_file.html')

@app.route('/farmers')
def farmers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Farmers')
    farmers = cursor.fetchall()
    conn.close()
    return render_template('farmers.html', farmers=farmers)

@app.route('/edit_farmer/<int:id>', methods=['GET', 'POST'])
def edit_farmer(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        unique_code = request.form['unique_code']
        name = request.form['name']
        surname = request.form['surname']
        id_number = request.form['id_number']
        bank_details = request.form['bank_details']
        contact_number = request.form['contact_number']
        address = request.form['address']
        household = request.form['household']
        location = request.form['location']
        land_size = request.form['land_size']
        
        cursor.execute('''
            UPDATE Farmers 
            SET UniqueCode = %s, Name = %s, Surname = %s, IDNumber = %s, BankDetails = %s, 
                ContactNumber = %s, Address = %s, Household = %s, Location = %s, LandSize = %s
            WHERE ID = %s
        ''', (unique_code, name, surname, id_number, bank_details, contact_number, address, household, location, land_size, id))
        conn.commit()
        conn.close()
        flash('Farmer updated successfully!', 'success')
        return redirect(url_for('farmers'))
    
    cursor.execute('SELECT * FROM Farmers WHERE ID = %s', (id,))
    farmer = cursor.fetchone()
    conn.close()
    return render_template('edit_farmer.html', farmer=farmer)

@app.route('/delete_farmer/<int:id>', methods=['GET', 'POST'])
def delete_farmer(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Farmers WHERE ID = %s', (id,))
    conn.commit()
    conn.close()
    flash('Farmer deleted successfully!', 'success')
    return redirect(url_for('farmers'))

import os
from flask import Flask

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define main folders and subfolders
folders = {
    'employees': ['contracts', 'personal_info'],
    'farmers': ['contracts', 'personal_info'],
    'procurements': ['invoices', 'purchase_orders'],
    'pictures': ['events', 'meetings'],
    'reports': ['financial', 'activity'],
    'administration': ['policies', 'guidelines'],
    'performance_monitors': ['individual', 'team'],
    'evaluation': ['reviews', 'assessments'] 
}

# Create folders if they don't exist
for main_folder, subfolders in folders.items():
    main_path = os.path.join(app.config['UPLOAD_FOLDER'], main_folder)
    if not os.path.exists(main_path):
        os.makedirs(main_path)
    for subfolder in subfolders:
        sub_path = os.path.join(main_path, subfolder)
        if not os.path.exists(sub_path):
            os.makedirs(sub_path)

from flask import Flask, request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename

@app.route('/upload_file/<main_folder>/<subfolder>', methods=['GET', 'POST'])
def upload_file(main_folder, subfolder):
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        if file:
            folder_path = os.path.join(app.config['UPLOAD_FOLDER'], main_folder, subfolder)
            if not os.path.exists(folder_path):
                flash('Folder does not exist', 'danger')
                return redirect(request.url)
            filename = secure_filename(file.filename)
            file.save(os.path.join(folder_path, filename))
            flash('File successfully uploaded', 'success')
            return redirect(url_for('dashboard'))
    return render_template('upload_file.html', main_folder=main_folder, subfolder=subfolder)

# Ensure the __main__ block is at the end
if __name__ == '__main__':
    app.run(debug=True, port=5000) 


     
           
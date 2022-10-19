from crypt import methods
from multiprocessing.sharedctypes import Value
from flask import Flask, request, render_template, url_for, redirect
import sqlite3

app = Flask(__name__)
database = 'handling.db'

@app.route('/')
def dashboard():
    movements = movements_query()
    return render_template('dashboard.html', movements=movements )

def movements_query():
    connie = sqlite3.connect(database)
    c = connie.cursor()
    c.execute("""
    SELECT * FROM movements
    """)
    all_movements = c.fetchall()
    return all_movements

@app.route('/add_movement', methods = ['GET', 'POST'])
def add_form():
    if request.method == 'GET':
        return render_template('add_movement.html')
    else:
        form_output = (
            request.form['registration'],
            request.form['arrival'],
            request.form['departure'])
        insert_to_db(form_output)

        return redirect('/')

def insert_to_db(form_output):
    connie = sqlite3.connect(database)
    c = connie.cursor()
    sql_insert_string = 'INSERT INTO movements (registration, arrival, departure) VALUES (?, ?, ?)'
    c.execute(sql_insert_string, form_output)
    connie.commit()
    connie.close()

@app.route('/erase_movement', methods = ['GET', 'POST'])
def erase_form():
    if request.method == 'GET':
        movements = movements_query()
        return render_template('erase_movement.html', movements=movements )

    else:
        form_output = (request.form['registration'])
        print (form_output)
        erase_from_db(form_output)

        return form_output #redirect('/')

def erase_from_db(form_output):
    connie = sqlite3.connect(database)
    c = connie.cursor()
    sql_erase_string = 'DELETE FROM movements WHERE registration = (?)'
    c.execute(sql_erase_string, form_output)
    connie.commit()
    connie.close()

def movements_query():
    connie = sqlite3.connect(database)
    c = connie.cursor()
    c.execute("""
    SELECT * FROM movements
    """)
    all_movements = c.fetchall()
    return all_movements



    
    


if __name__ == '__main__':
    app.run()
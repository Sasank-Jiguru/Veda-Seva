from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

app.secret_key = "vedaseva"

# ================= DATABASE =================

def init_db():

    conn = sqlite3.connect('veda.db')

    c = conn.cursor()

    # DEVOTEES

    c.execute('''

    CREATE TABLE IF NOT EXISTS devotees (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,

        phone TEXT,

        dob TEXT,

        birthtime TEXT,

        birthplace TEXT,

        purpose TEXT,

        dosha TEXT,

        pariharam TEXT

    )

    ''')

    # REMINDERS

    c.execute('''

    CREATE TABLE IF NOT EXISTS reminders (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        devotee TEXT,

        work TEXT,

        reminder_date TEXT,

        reminder_time TEXT

    )

    ''')

    # BOOKINGS

    c.execute('''

    CREATE TABLE IF NOT EXISTS bookings (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        devotee TEXT,

        service TEXT,

        booking_date TEXT,

        booking_time TEXT,

        notes TEXT

    )

    ''')

    conn.commit()

    conn.close()

# ================= DOSHA DATA =================

DOSHA_PARIAHARAM = {

    "కుజ దోషం": "అంగారక జపం | 7000 సార్లు | మంగళవారం",

    "శని దోషం": "శని శాంతి హోమం | 11 సార్లు | శనివారం",

    "కాలసర్ప దోషం": "రాహు కేతు పూజ | నాగుల చవితి",

    "పితృ దోషం": "పితృ శాంతి హోమం | అమావాస్య"

}

# ================= LOGIN =================

@app.route('/login', methods=['GET', 'POST'])

def login():

    if request.method == 'POST':

        username = request.form['username']

        password = request.form['password']

        if username == "admin" and password == "1234":

            session['user'] = username

            return redirect('/dashboard')

    return render_template('login.html')

# ================= LOGOUT =================

@app.route('/logout')

def logout():

    session.pop('user', None)

    return redirect('/login')

# ================= DASHBOARD =================

@app.route('/')

@app.route('/dashboard')

def dashboard():

    if 'user' not in session:

        return redirect('/login')

    conn = sqlite3.connect('veda.db')

    c = conn.cursor()

    c.execute("SELECT * FROM devotees")

    devotees = c.fetchall()

    c.execute("SELECT * FROM reminders")

    reminders = c.fetchall()

    c.execute("SELECT * FROM bookings")

    bookings = c.fetchall()

    conn.close()

    return render_template(

        'dashboard.html',

        devotees=devotees,

        reminders=reminders,

        bookings=bookings

    )

# ================= DEVOTEES =================

@app.route('/devotees')

def devotees():

    if 'user' not in session:

        return redirect('/login')

    conn = sqlite3.connect('veda.db')

    c = conn.cursor()

    c.execute("SELECT * FROM devotees")

    data = c.fetchall()

    conn.close()

    return render_template(

        'devotees.html',

        devotees=data

    )

# ================= ADD DEVOTEE =================

@app.route('/add', methods=['POST'])

def add():

    name = request.form['name']

    phone = request.form['phone']

    dob = request.form['dob']

    birthtime = request.form['birthtime']

    birthplace = request.form['birthplace']

    purpose = request.form['purpose']

    dosha = request.form['dosha']

    if dosha in DOSHA_PARIAHARAM:

        pariharam = DOSHA_PARIAHARAM[dosha]

    else:

        pariharam = "ప్రత్యేక పరిహారం అవసరం"

    conn = sqlite3.connect('veda.db')

    c = conn.cursor()

    c.execute(

        '''

        INSERT INTO devotees

        (name, phone, dob, birthtime, birthplace, purpose, dosha, pariharam)

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)

        ''',

        (name, phone, dob, birthtime, birthplace, purpose, dosha, pariharam)

    )

    conn.commit()

    conn.close()

    return redirect('/devotees')

# ================= DELETE =================

@app.route('/delete/<int:id>')

def delete(id):

    conn = sqlite3.connect('veda.db')

    c = conn.cursor()

    c.execute("DELETE FROM devotees WHERE id=?", (id,))

    conn.commit()

    conn.close()

    return redirect('/devotees')

# ================= EDIT =================

@app.route('/edit/<int:id>')

def edit(id):

    conn = sqlite3.connect('veda.db')

    c = conn.cursor()

    c.execute("SELECT * FROM devotees WHERE id=?", (id,))

    devotee = c.fetchone()

    conn.close()

    return render_template(

        'edit.html',

        devotee=devotee

    )

# ================= UPDATE =================

@app.route('/update/<int:id>', methods=['POST'])

def update(id):

    name = request.form['name']

    phone = request.form['phone']

    dosha = request.form['dosha']

    pariharam = DOSHA_PARIAHARAM.get(

        dosha,

        "ప్రత్యేక పరిహారం అవసరం"

    )

    conn = sqlite3.connect('veda.db')

    c = conn.cursor()

    c.execute(

        '''

        UPDATE devotees

        SET name=?,
        phone=?,
        dosha=?,
        pariharam=?

        WHERE id=?

        ''',

        (name, phone, dosha, pariharam, id)

    )

    conn.commit()

    conn.close()

    return redirect('/devotees')

# ================= PANCHANGAM =================

@app.route('/panchangam', methods=['GET', 'POST'])

def panchangam():

    selected_date = ""

    data = {}

    if request.method == 'POST':

        selected_date = request.form['date']

        data = {

            "tithi": "శుక్ల పక్ష ద్వాదశి",

            "varam": "శనివారం",

            "nakshatram": "శ్రవణం",

            "rahukalam": "09:00 - 10:30",

            "yamagandam": "01:30 - 03:00",

            "durmuhurtham": "08:45 - 09:30"

        }

    return render_template(

        'panchangam.html',

        data=data,

        selected_date=selected_date

    )

# ================= HOROSCOPE =================

@app.route('/horoscope', methods=['GET', 'POST'])

def horoscope():

    result = {}

    if request.method == 'POST':

        dob = request.form['dob']

        birthtime = request.form['birthtime']

        birthplace = request.form['birthplace']

        result = {

            "nakshatram": "రోహిణి",

            "rasi": "వృషభం",

            "lagnam": "మేషం",

            "dosham": "కుజ దోషం",

            "pariharam": "అంగారక జపం | మంగళవారం"

        }

    return render_template(

        'horoscope.html',

        result=result

    )

# ================= BOOKINGS =================

@app.route('/bookings')

def bookings():

    conn = sqlite3.connect('veda.db')

    c = conn.cursor()

    c.execute("SELECT * FROM bookings")

    data = c.fetchall()

    conn.close()

    return render_template(

        'bookings.html',

        bookings=data

    )

# ================= ADD BOOKING =================

# ================= ADD BOOKING =================

@app.route('/add_booking', methods=['POST'])

def add_booking():

    devotee = request.form['devotee']

    service = request.form['service']

    booking_date = request.form['booking_date']

    booking_time = request.form['booking_time']

    notes = request.form['notes']

    conn = sqlite3.connect('veda.db')

    c = conn.cursor()

    # CHECK DUPLICATE SLOT

    c.execute(

        '''

        SELECT * FROM bookings

        WHERE booking_date=?

        AND booking_time=?

        ''',

        (booking_date, booking_time)

    )

    existing_booking = c.fetchone()

    # SLOT ALREADY BOOKED

    if existing_booking:

        conn.close()

        return """

        <h1 style='color:red;text-align:center;margin-top:50px;'>

        ⚠️ ఈ Slot ఇప్పటికే Book అయింది

        </h1>

        <div style='text-align:center;'>

        <a href='/bookings'>

        <button style='padding:15px;background:red;color:white;border:none;border-radius:10px;'>

        వెనక్కి వెళ్ళండి

        </button>

        </a>

        </div>

        """

    # INSERT NEW BOOKING

    c.execute(

        '''

        INSERT INTO bookings

        (devotee, service, booking_date, booking_time, notes)

        VALUES (?, ?, ?, ?, ?)

        ''',

        (devotee, service, booking_date, booking_time, notes)

    )

    conn.commit()

    conn.close()

    return redirect('/bookings')

# ================= JAPALU =================

@app.route('/japalu')

def japalu():

    return render_template('japalu.html')

# ================= HOMALU =================

@app.route('/homalu')

def homalu():

    return render_template('homalu.html')

# ================= DOSHALU =================

@app.route('/doshalu')

def doshalu():

    return render_template(

        'doshalu.html',

        doshalu=DOSHA_PARIAHARAM

    )

# ================= REMINDERS =================

@app.route('/reminders')

def reminders():

    conn = sqlite3.connect('veda.db')

    c = conn.cursor()

    c.execute("SELECT * FROM reminders")

    data = c.fetchall()

    conn.close()

    return render_template(

        'reminders.html',

        reminders=data

    )

# ================= ADD REMINDER =================

@app.route('/add_reminder', methods=['POST'])

def add_reminder():

    devotee = request.form['devotee']

    work = request.form['work']

    reminder_date = request.form['reminder_date']

    reminder_time = request.form['reminder_time']

    conn = sqlite3.connect('veda.db')

    c = conn.cursor()

    c.execute(

        '''

        INSERT INTO reminders

        (devotee, work, reminder_date, reminder_time)

        VALUES (?, ?, ?, ?)

        ''',

        (devotee, work, reminder_date, reminder_time)

    )

    conn.commit()

    conn.close()

    return redirect('/reminders')

# ================= SETTINGS =================

@app.route('/settings')

def settings():

    return render_template('settings.html')

# ================= MAIN =================

if __name__ == "__main__":

    init_db()

    app.run(

        host="0.0.0.0",

        port=int(os.environ.get("PORT", 8080)),

        debug=False

    )
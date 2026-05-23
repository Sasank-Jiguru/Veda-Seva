from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)

app.secret_key = "vedaseva"

# ================= DATABASE =================

def init_db():

    conn = sqlite3.connect('veda.db')

    c = conn.cursor()

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

    c.execute('''

    CREATE TABLE IF NOT EXISTS reminders (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        devotee TEXT,

        work TEXT,

        reminder_date TEXT,

        reminder_time TEXT

    )

    ''')

    conn.commit()

    conn.close()

# ================= DOSHA =================

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

    conn.close()

    return render_template(
        'dashboard.html',
        devotees=devotees,
        reminders=reminders
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

    return render_template('devotees.html', devotees=data)

# ================= ADD =================

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

# ================= PAGES =================

@app.route('/japalu')

def japalu():

    return render_template('japalu.html')

@app.route('/homalu')

def homalu():

    return render_template('homalu.html')

@app.route('/doshalu')

def doshalu():

    return render_template(
        'doshalu.html',
        doshalu=DOSHA_PARIAHARAM
    )

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

@app.route('/settings')

def settings():

    return render_template('settings.html')

# ================= REMINDER ADD =================

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

# ================= MAIN =================

if __name__ == '__main__':

    init_db()

    app.run(debug=True)
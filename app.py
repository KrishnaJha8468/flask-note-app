from flask import Flask, request, session, redirect, render_template_string
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SESSION_COOKIE_HTTPONLY'] = True

def get_db_connection():
    conn = sqlite3.connect('notes.db')
    conn.row_factory = sqlite3.Row
    return conn

# Templates as strings for simplicity
register_template = '''
<!doctype html>
<title>Register</title>
<h2>Register</h2>
<form method="post">
  Username: <input type="text" name="username" required><br>
  Password: <input type="password" name="password" required><br>
  <input type="submit" value="Register">
</form>
<a href="/login">Login</a>
'''

login_template = '''
<!doctype html>
<title>Login</title>
<h2>Login</h2>
<form method="post">
  Username: <input type="text" name="username" required><br>
  Password: <input type="password" name="password" required><br>
  <input type="submit" value="Login">
</form>
<a href="/register">Register</a>
<p style="color:red;">{{ error }}</p>
'''

dashboard_template = '''
<!doctype html>
<title>Dashboard</title>
<h2>Welcome, {{ user }}!</h2>
<h3>Your Notes:</h3>
<ul>
  {% for note in notes %}
    <li>{{ note['note'] }}</li>
  {% else %}
    <li>No notes yet.</li>
  {% endfor %}
</ul>
<form method="post" action="/add_note">
  <input type="text" name="note" placeholder="New note" required>
  <input type="submit" value="Add Note">
</form>
<br>
<a href="/logout">Logout</a>
'''

@app.route('/')
def index():
    if 'user' in session:
        return redirect('/dashboard')
    else:
        return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return "Username already exists. Please choose another."
        conn.close()
        return redirect('/login')
    return render_template_string(register_template)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session['user'] = username
            return redirect('/dashboard')
        else:
            error = "Invalid credentials"
    return render_template_string(login_template, error=error)

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        conn = get_db_connection()
        notes = conn.execute("SELECT * FROM notes WHERE username = ?", (session['user'],)).fetchall()
        conn.close()
        return render_template_string(dashboard_template, notes=notes, user=session['user'])
    return redirect('/login')

@app.route('/add_note', methods=['POST'])
def add_note():
    if 'user' in session:
        note = request.form['note']
        conn = get_db_connection()
        conn.execute("INSERT INTO notes (username, note) VALUES (?, ?)", (session['user'], note))
        conn.commit()
        conn.close()
        return redirect('/dashboard')
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)

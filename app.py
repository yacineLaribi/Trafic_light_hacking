from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Insecure key for demo purposes

# Dummy database setup
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    c.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', 'h4rdp455w0rd')")
    conn.commit()
    conn.close()

init_db()

# Home Page
@app.route("/")
def index():
    return render_template("index.html")

# Login with SQL Injection vulnerability
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        c.execute(query)  # Vulnerable to SQL Injection
        user = c.fetchone()
        conn.close()

        if user:
            session["admin"] = True
            return redirect("/admin")
        else:
            return "Invalid credentials"

    return render_template("login.html")

# Admin Panel
@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect("/login")
    return render_template("admin.html")

# Change Traffic Light Timing
@app.route("/change-timing", methods=["POST"])
def change_timing():
    if not session.get("admin"):
        return "Unauthorized", 403

    green = request.form.get("green")
    red = request.form.get("red")

    if green == "999" and red == "999" :
        return "Warning: Security breach detected! System resetting..."

    if green == "60" and red == "30":
        return "Flag: CTF{TR4FF1C_L1GHT_HACKED}"
    
    return "Timing changed successfully"

if __name__ == "__main__":
    app.run(debug=True)

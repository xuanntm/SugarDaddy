from flask import Flask, redirect, url_for, session, request, jsonify, render_template
from authlib.integrations.flask_client import OAuth
import os
import secrets
from datetime import datetime, timedelta
import psycopg2  # For PostgreSQL interaction
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Database Configuration (Replace with your PostgreSQL credentials)
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

app = Flask(__name__, template_folder="../asset/pages")
app.secret_key = os.urandom(24)

# OAuth2 Configuration (Replace with your provider's details)
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',  # Or the correct base URL
    client_kwargs={'scope': 'email profile'}, # Use string for scope
)

# Role Management (Simplified example – you'll likely use a database)
roles = {
    "investor@example.com": "investor",  # Replace with actual email addresses
    "analyst@example.com": "analyst",
    "virutforever@gmail.com": "analyst",
}

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def get_user_role(email):
    """Retrieves the role of a user based on their email."""
    # In a real app, you would fetch this from a database.
    return roles.get(email)

@app.route('/')
def index():
    if 'user' in session:
        email = session['user']['email']
        role = get_user_role(email)
        return f"Hello, {email}! You are a {role}."  # Or redirect to appropriate page
    return '<a href="/login">Login with Google</a>'

@app.route('/login')
def login():
    redirect_uri = url_for('authorized', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorized')
def authorized():
    try:
        token = google.authorize_access_token()
        userinfo = google.get('userinfo', token=token).json()  # Get userinfo
        session['user'] = userinfo
        # ... (rest of your authorized logic - role check, redirect, etc.)
        email = session['user']['email']
        role = get_user_role(email)
        if role:  # Check if the user has a defined role
            return redirect(url_for('index'))  # Redirect to the main page
        else:
            return "You do not have permission to access this application.", 403 # Unauthorized

    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

# Example protected route (Investor only)
@app.route('/investor_dashboard')
def investor_dashboard():
    if 'user' not in session or get_user_role(session['user']['email']) != 'investor':
        return "You do not have permission to access this page.", 403
    return "Welcome to the Investor Dashboard!"

# Example protected route (Analyst only)
@app.route('/analyst_dashboard', methods=['GET', 'POST'])
def analyst_dashboard():
    # if 'user' not in session or session.get('role') != 'analyst':
    if 'user' not in session or get_user_role(session['user']['email']) != 'analyst':
        return "Unauthorized", 403

    conn = get_db_connection()
    if not conn:
        return "Database connection error", 500

    try:
        cur = conn.cursor()
        # Example query (replace with your actual query)
        cur.execute("SELECT * FROM service_management.remit_service")  # Replace your_table
        data = cur.fetchall()
        cur.close()
        conn.close()

        if request.method == 'POST':  # Handle refresh button click
            return jsonify(data)  # Return data as JSON for AJAX update
        print(jsonify(data))
        return render_template('analyst_dashboard.html', data=data)  # Initial page load

    except psycopg2.Error as e:
        print(f"Database query error: {e}")
        conn.close()  # Close connection in case of error
        return "Database query error", 500

if __name__ == '__main__':
    app.run(debug=True)  # Set debug=False in production
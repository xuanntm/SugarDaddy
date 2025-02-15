from flask import Flask, redirect, url_for, session, request, jsonify
from authlib.integrations.flask_client import OAuth
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
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
@app.route('/analyst_dashboard')
def analyst_dashboard():
    if 'user' not in session or get_user_role(session['user']['email']) != 'analyst':
        return "You do not have permission to access this page.", 403
    return "Welcome to the Analyst Dashboard!"

if __name__ == '__main__':
    app.run(debug=True)  # Set debug=False in production
import os

from flask import Flask, render_template, redirect, url_for, session, request

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or 'my_secret_key'


# TODO('/'): Decide whether to use 'home' or 'home_landing' as the initial route

# Define a function that checks if the user is authenticated
def login_required(func):
    def wrapper(*args, **kwargs):
        if 'email' not in session:
            return redirect(url_for('login', next=request.path))
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__

    return wrapper


# Define a route for the homepage
@app.route('/')
def initial_route():
    return render_template('index.html')


@app.route('/home')
@login_required
def home():
    return render_template('home.html', name=session['name'])


# Define a route for a coming soon page
@app.route('/coming-soon')
def coming_soon():
    return render_template('coming_soon.html')


users = {
    'john@example.com': {'password': 'password1', 'name': 'John'},
    'mary@example.com': {'password': 'password2', 'name': 'Mary'},
    'david@example.com': {'password': 'password3', 'name': 'David'},
}


# Define a route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Check if user is already logged in
    if 'email' in session:
        return redirect(url_for('home_landing'))

    # Check if user submitted login form
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if user credentials are valid
        if email in users and password == users[email]['password']:
            session['email'] = email
            session['name'] = users[email]['name']
            return redirect(url_for('home'))

        # If credentials are invalid, show error message
        error = 'Invalid login credentials. Please try again.'
        return render_template('login.html', error=error)

    # If user has not submitted form, show login page
    return render_template('login.html')


# Define logout route
@app.route('/logout')
def logout():
    # Remove user session data
    session.pop('username', None)
    session.pop('name', None)

    # Redirect user to login page
    return redirect(url_for('login'))


@app.route('/home_landing')
@login_required
def home_landing():
    return render_template('home_landing.html', name=session['name'])


@app.route('/services')
@login_required
def services():
    return render_template('services.html', name=session['name'])


@app.route('/support')
@login_required
def support():
    return render_template('support.html', name=session['name'])


if __name__ == '__main__':
    app.run(debug=True)

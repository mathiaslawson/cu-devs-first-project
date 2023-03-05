from flask import Flask, render_template

app = Flask(__name__)

user = None


def check_auth(fn):
    def closure():
        if user is not None:
            return fn()
        # TODO(Login): Redirect to login page
        return render_template('login-in.html')

    closure.__name__ = fn.__name__

    return closure


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/home')
@check_auth
def home_landing():
    return render_template('home-page.html')


@app.route('/services')
# @check_auth
def services():
    return render_template('coming_soon.html')


@app.route('/support')
# @check_auth
def support():
    return render_template('coming_soon.html')


@app.route('/login')
def login():
    return render_template('login-in.html')


if __name__ == '__main__':
    app.run(debug=True)

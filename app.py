from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def login():  # put application's code here
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/logout')
def logout():
    return render_template('login.html')


@app.route('/preferences')
def preferences():
    return render_template('preferences-input.html')


@app.route('/results')
def results():
    return render_template('results.html')


if __name__ == '__main__':
    app.run()

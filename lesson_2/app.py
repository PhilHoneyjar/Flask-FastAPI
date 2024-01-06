from flask import Flask, render_template, request, make_response, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/welcome', methods=['POST'])
def welcome():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        response = make_response(redirect(url_for('greet')))
        response.set_cookie('user', f'{name} - {email}')
        return response


@app.route('/greet')
def greet():
    user_cookie = request.cookies.get('user')
    if user_cookie:
        username = user_cookie.split(' - ')[0]
        return render_template('welcome.html', username=username)
    else:
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('index')))
    response.set_cookie('user', '', expires=0)
    return response


if __name__ == '__main__':
    app.run(debug=True)

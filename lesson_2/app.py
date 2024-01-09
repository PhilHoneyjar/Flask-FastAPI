from flask import Flask, render_template, request, make_response, redirect, url_for

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        response = make_response(redirect(url_for('greet')))
        response.set_cookie('username', name)
        response.set_cookie('useremail', email)
        return response
    return render_template('index.html')


@app.route('/greet', methods=['GET', 'POST'])
def greet():
    if request.method == 'POST':
        response = make_response(redirect(url_for('index')))
        response.delete_cookie('username')
        response.delete_cookie('useremail')
        return response

    username = request.cookies.get('username')
    useremail = request.cookies.get('useremail')

    if not (username and useremail):
        return redirect(url_for('index'))

    return render_template('welcome.html', username=username, useremail=useremail)


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/clothing')
def clothing():
    return render_template('categories/clothing.html')


@app.route('/shoes')
def shoes():
    return render_template('categories/shoes.html')


@app.route('/clothing/jackets')
def jacket():
    return render_template('categories/clothing/jackets.html')


@app.route('/clothing/trousers')
def trousers():
    return render_template('categories/clothing/trousers.html')


@app.route('/shoes/boots')
def boots():
    return render_template('categories/shoes/boots.html')


@app.route('/shoes/sneakers')
def sneakers():
    return render_template('categories/shoes/sneakers.html')


if __name__ == '__main__':
    app.run(debug=True)

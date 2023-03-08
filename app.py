from flask import *
from flask_pymongo import PyMongo
from flask_bootstrap import Bootstrap
import pymongo
import os
from dotenv import load_dotenv



# loading environment from .env file

app_path = os.path.join(os.path.dirname(__file__), '.')
dotenv_path = os.path.join(app_path, '.env')
load_dotenv(dotenv_path)


app = Flask(__name__)
app.config['MONGO_URI'] = os.environ.get("MONGO_URI")
app.config['SECRET_KEY'] = "SomeSecret"
Bootstrap(app)
mongo = PyMongo(app)
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add', methods = ['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    elif request.method == 'POST':
        product = {}
        for item in request.form:
            product[item] = request.form[item]
        mongo.db.products.insert_one(product)
        return redirect('/')

@app.route('/buy', methods = ['GET', 'POST'])
def buy():
    if request.method == 'GET':
        session['items'] = {}
        allProducts = mongo.db.products.find()
        return render_template('buy.html', products = allProducts)
    elif request.method == 'POST':
        doc = {}
        for item in request.form:
            if request.form[item] and int(request.form[item]) != 0:
                doc[item] = request.form[item]
        session['items'] = doc
        return redirect('/checkout')

@app.route('/checkout')
def checkout():
    total = 0
    cart_items = []
    for id in session['items']:
        product = mongo.db.products.find_one({'_id': ObjectId(id)})
        product['quantity'] = session['items'][id]
        product['total'] = int(product['price']) * int(product['quantity'])
        cart_items.append(product)
        total += product['total']
    return render_template('checkout.html', products = cart_items, total = total)

if __name__ == '__main__':
    app.run(debug = True)


from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import random
import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'stocks.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Stock model
class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

# Function to create database tables
def create_tables():
    with app.app_context():
        db.create_all()

# Initialize the database and tables
def initialize_db():
    if not os.path.exists(os.path.join(app.instance_path, 'stocks.db')):
        create_tables()

# Ensure the instance folder exists
if not os.path.exists(app.instance_path):
    os.makedirs(app.instance_path)

initialize_db()

@app.route('/create_tables', methods=['POST'])
def create_tables_route():
    create_tables()
    return jsonify({"message": "Database tables created successfully"}), 201

@app.route('/simulate', methods=['POST'])
def simulate():
    num_records = request.json.get('num_records', 10)
    now = datetime.datetime.now()

    for _ in range(num_records):
        ticker = random.choice(['AAPL', 'GOOGL', 'MSFT'])
        price = round(random.uniform(100, 1500), 2)
        volume = random.randint(100000, 5000000)
        stock = Stock(ticker=ticker, price=price, volume=volume, date=now)
        db.session.add(stock)
    
    db.session.commit()
    return jsonify({"message": "Simulation data added successfully"}), 201

@app.route('/stocks', methods=['GET'])
def get_stocks():
    stocks = Stock.query.all()
    return jsonify([{
        "id": stock.id,
        "ticker": stock.ticker,
        "price": stock.price,
        "volume": stock.volume,
        "date": stock.date.isoformat()
    } for stock in stocks])

@app.route('/price_reversion', methods=['GET'])
def price_reversion():
    stocks = Stock.query.all()
    results = []

    average_price = Stock.query.with_entities(db.func.avg(Stock.price)).scalar()
    
    for stock in stocks:
        action = 'Buy' if stock.price < average_price else 'Hold'
        results.append({
            "ticker": stock.ticker,
            "price": stock.price,
            "action": action
        })
    
    return jsonify(results)

@app.route('/view_db', methods=['GET'])
def view_db():
    stocks = Stock.query.all()
    return jsonify([{
        "id": stock.id,
        "ticker": stock.ticker,
        "price": stock.price,
        "volume": stock.volume,
        "date": stock.date.isoformat()
    } for stock in stocks])

if __name__ == '__main__':
    app.run(debug=True)

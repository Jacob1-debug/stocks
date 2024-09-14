from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import random
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stocks.db'
db = SQLAlchemy(app)

# Define Stock model
class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

# Create database and tables
@app.before_first_request
def create_tables():
    db.create_all()

# Simulate route to add fake data
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

# Route to get all stocks
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

# Route to simulate price reversion strategy
@app.route('/price_reversion', methods=['GET'])
def price_reversion():
    stocks = Stock.query.all()
    results = []

    for stock in stocks:
        # Simple mean reversion strategy: Buy if the price is lower than the average price
        average_price = Stock.query.with_entities(db.func.avg(Stock.price)).scalar()
        action = 'Buy' if stock.price < average_price else 'Hold'
        results.append({
            "ticker": stock.ticker,
            "price": stock.price,
            "action": action
        })
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)

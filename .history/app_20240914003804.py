from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from faker import Faker

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
db = SQLAlchemy(app)
fake = Faker()

# Define your database models here
class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<Stock {self.ticker}>"

# Create the database and tables
@app.before_first_request
def create_tables():
    db.create_all()

# Route to simulate adding fake data
@app.route('/simulate', methods=['POST'])
def simulate():
    num_records = request.json.get('num_records', 100)
    for _ in range(num_records):
        stock = Stock(
            ticker=fake.company_suffix(),
            price=fake.random_number(digits=5),
            volume=fake.random_number(digits=4),
            date=fake.date_time_this_decade()
        )
        db.session.add(stock)
    db.session.commit()
    return jsonify({"message": "Simulation data added successfully"}), 201

# Route to fetch all stocks
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
    for stock in stocks:
        # Simple mean reversion strategy: Buy if price is below mean, sell if above
        mean_price = Stock.query.with_entities(db.func.avg(Stock.price)).scalar()
        if stock.price < mean_price:
            action = 'Buy'
        elif stock.price > mean_price:
            action = 'Sell'
        else:
            action = 'Hold'
        
        results.append({
            "ticker": stock.ticker,
            "price": stock.price,
            "action": action
        })
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)

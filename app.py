from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
import stripe
import requests
import os

app = Flask(__name__)
CORS(app)

# Configurations
app.config['JWT_SECRET_KEY'] = 'your-jwt-secret-key'  # Change this to a random secret key
jwt = JWTManager(app)

# Stripe Configuration
stripe.api_key = 'your-stripe-secret-key'

@app.route('/')
def home():
    return render_template('index.html')  # Renders the homepage

# User Sign-up Route (Simple Example)
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data['username']
    password = data['password']
    # For simplicity, we're just returning the data (You would store this in a database)
    return jsonify(message="User signed up successfully", user=username)

# User Login Route (Simple Example with JWT)
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    
    # For simplicity, assuming login is successful without database validation
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

# Crypto Prices API (Using CoinGecko API)
@app.route('/api/crypto-prices')
def crypto_prices():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 10}
    response = requests.get(url, params=params)
    data = response.json()
    return jsonify(data)

# Payment Route (Stripe)
@app.route('/api/payment', methods=['POST'])
def payment():
    try:
        data = request.json
        amount = data['amount']  # The amount to charge in cents

        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd'
        )
        return jsonify(client_secret=intent['client_secret'])
    except Exception as e:
        return jsonify(error=str(e)), 403

if __name__ == '__main__':
    app.run(debug=True)

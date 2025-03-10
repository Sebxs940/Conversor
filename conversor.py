import requests
import json
import os
import sys
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os

# Initialize Flask app with the correct template folder
template_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, template_folder='templates', static_folder='static')

# API key for ExchangeRate-API (you'll need to sign up for a free API key)
API_KEY = os.getenv('API_KEY')  # Replace with your API key from https://www.exchangerate-api.com/

def get_exchange_rates(base_currency="USD"):
    """Get exchange rates from the API"""
    try:
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base_currency}"
        response = requests.get(url)
        data = response.json()
        
        if data["result"] == "success":
            return data["conversion_rates"]
        else:
            print(f"API Error: {data.get('error-type', 'Unknown error')}")
            return None
    except Exception as e:
        print(f"Error fetching exchange rates: {e}")
        return None

def convert_currency(amount, from_currency, to_currency):
    """Convert an amount from one currency to another"""
    rates = get_exchange_rates(from_currency)
    
    if rates and to_currency in rates:
        converted_amount = amount * rates[to_currency]
        return converted_amount
    else:
        return None

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    """API endpoint for currency conversion"""
    try:
        data = request.get_json()
        amount = float(data.get('amount', 1))
        from_currency = data.get('from', 'USD')
        to_currency = data.get('to', 'COP')
        
        result = convert_currency(amount, from_currency, to_currency)
        
        if result is not None:
            return jsonify({
                'success': True,
                'amount': amount,
                'from': from_currency,
                'to': to_currency,
                'result': result,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Conversion failed. Please check your currencies.'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == "__main__":
    print("Starting web server for Currency Converter...")
    print("Get your API key from https://www.exchangerate-api.com/ and replace 'YOUR_API_KEY' in the script")
    print("Access the converter at http://localhost:5000")
    app.run(debug=True)

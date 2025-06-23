import requests
import json
import os
import sys
from flask import Flask, render_template, request, jsonify
from datetime import datetime

# Initialize Flask app with the correct template folder
template_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, template_folder='templates', static_folder='static')

# API key for ExchangeRate-API (set this as env variable)
API_KEY = os.getenv('API_KEY')

def get_exchange_rates(base_currency="USD"):
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
    rates = get_exchange_rates(from_currency)
    if rates and to_currency in rates:
        converted_amount = amount * rates[to_currency]
        return converted_amount
    else:
        return None

def get_client_ip():
    """Obtener la IP real del visitante, incluso detrás de proxy"""
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
    return ip

@app.route('/')
def index():
    ip = get_client_ip()
    print(f"🔍 Visita detectada desde IP: {ip} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    try:
        ip = get_client_ip()
        print(f"💱 Solicitud de conversión desde IP: {ip} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

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
    print("🚀 Iniciando servidor web para Currency Converter...")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)

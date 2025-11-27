from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS # Needed for local testing, but good practice

app = Flask(__name__)
# Enable CORS for all routes (important for front-end to call API)
CORS(app)

def sip_calculator(monthly_investment, annual_rate, time_period):
    """
    Calculates the Future Value of a SIP.
    
    Formula: FV = P * [((1 + i)^n - 1) / i] * (1 + i)
    Where:
    P = Monthly Investment
    i = Monthly Rate of Return = Annual Rate / 12 / 100
    n = Number of Months = Time Period in Years * 12
    """
    
    # Convert annual rate % to monthly rate (decimal)
    monthly_rate = (annual_rate / 100) / 12
    # Convert time period in years to total number of months
    number_of_months = time_period * 12
    
    # SIP Future Value Calculation
    if monthly_rate == 0:
        # Simple case if rate is 0 (though unlikely in real SIP)
        future_value = monthly_investment * number_of_months
    else:
        # The main SIP Future Value formula
        future_value = monthly_investment * (
            ((1 + monthly_rate) ** number_of_months - 1) / monthly_rate
        ) * (1 + monthly_rate)
        
    invested_amount = monthly_investment * number_of_months
    estimated_gain = future_value - invested_amount
    
    return {
        "future_value": future_value,
        "invested_amount": invested_amount,
        "estimated_gain": estimated_gain
    }

@app.route('/')
def serve_frontend():
    """Serves the frontend HTML file."""
    # In a real deployment, you might use a web server (like Nginx) 
    # to serve the static HTML, but for simplicity, we serve it here.
    with open('frontend.html', 'r') as f:
        html_content = f.read()
    return html_content

@app.route('/calculate', methods=['POST'])
def calculate_api():
    """API endpoint to handle the SIP calculation request."""
    data = request.get_json()
    
    try:
        monthly_investment = float(data['monthly_investment'])
        annual_rate = float(data['annual_rate'])
        time_period = float(data['time_period'])
    except (TypeError, KeyError, ValueError):
        return jsonify({"error": "Invalid input parameters"}), 400

    result = sip_calculator(monthly_investment, annual_rate, time_period)
    
    # Rounding the results for cleaner presentation
    result['future_value'] = round(result['future_value'], 2)
    result['invested_amount'] = round(result['invested_amount'], 2)
    result['estimated_gain'] = round(result['estimated_gain'], 2)
    
    return jsonify(result)

if __name__ == '__main__':
    # Running on all interfaces (0.0.0.0) and port 5000 for Docker/Kubernetes deployment
    app.run(host='0.0.0.0', port=5000)

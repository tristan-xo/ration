from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Airtable Configuration
AIRTABLE_BASE_ID = "appYfDpjp590SPSaq"
AIRTABLE_TABLE_NAME = "transactions"
AIRTABLE_PAT = "patJDZhapgtdMckqU.d052a80071d028c5901fd9e081c0ab6c4a02fd856f5735942cf0e2602c5f83c2"

# Airtable API URL
AIRTABLE_URL = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"

# Headers for Airtable API
HEADERS = {
    "Authorization": f"Bearer {AIRTABLE_PAT}",
    "Content-Type": "application/json"
}

# Stock Prices (per kg)
STOCK_PRICES = {
    "rice": 2,    # ₹2 per kg
    "wheat": 10,  # ₹10 per kg
    "sugar": 20,  # ₹20 per kg
    "dal": 15     # ₹15 per kg
}

@app.route("/transactions", methods=["GET"])
def get_transactions():
    user_id = request.args.get("user_id")  # Fetch phone number as user_id

    if not user_id:
        return jsonify({"error": "Missing user_id parameter"}), 400

    # Airtable filter formula to match user_id
    filter_formula = f"{{user_id}}='{user_id}'"
    params = {"filterByFormula": filter_formula}

    try:
        response = requests.get(AIRTABLE_URL, headers=HEADERS, params=params)
        data = response.json()

        if "records" not in data or len(data["records"]) == 0:
            return jsonify({"error": "No transactions found"}), 404

        transactions = []
        total_bill = 0  # Initialize total bill

        for record in data["records"]:
            fields = record.get("fields", {})

            stock_name = fields.get("stocks", "").lower()
            if not stock_name:  # Skip if stocks field is empty
                continue

            quantity = fields.get("quantity_taken", 0)
            price = STOCK_PRICES.get(stock_name, 0) * quantity  # Calculate price
            total_bill += price  # Add to total bill

            transactions.append({
                "date": fields.get("date", "----"),
                "stocks": fields.get("stocks", "----"),
                "quantity_taken": quantity,
                "price": price  # New calculated price field
            })

        # Return transactions with total bill separately
        return jsonify({"transactions": transactions, "total_bill": total_bill})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, Float
from scraper import get_product

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return "Welcome to the E-commerce Product Scraper"

@app.route('/scrape', methods=['GET', 'POST'])
def scrape():
    if request.method == 'POST':
        product_url = request.form["product_url"]
        try:
            results = get_product(product_url)
            return jsonify(results)
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    return render_template('index.html')


if __name__ == "__main__":
    app.run()


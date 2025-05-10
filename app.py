# app.py
from flask import Flask, request, jsonify
import json
from bson import json_util
# from config import *

# Load the Flask
app = Flask(__name__)

# Home Page
@app.route("/")
def home():
    return "Hello, Flask!"

# Home Page
@app.route("/about")
def about():
    return "Hello, About us!"

# # Register the product blueprint
# app.register_blueprint(product_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


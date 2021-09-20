from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect
import dao
from backend import *
from customer import Customer

app = Flask(__name__)

@app.route('/get_customer/<id_of_customer>', methods=['GET'])
def get_customer(id_of_customer):
    customerinfo = dao.get_customer(id_of_customer)
    return jsonify(customerinfo.__dict__())

@app.route('/delete_customer/<id_of_customer>', methods=['DELETE'])
def delete_customer(id_of_customer):
    return jsonify(dao.delete_customer(id_of_customer))

@app.route("/update_customer_credit/<name>/<credit>", methods=['PUT'])
def update_customer_credit(name, credit):
    return jsonify(dao.update_customer(name,credit))

@app.route('/add_customer', methods=['POST'])
def add_customer():
    req_data = request.get_json()
    customer = Customer(req_data["customer_id"], req_data["customer_name"], req_data["password"], req_data["credit"])
    return jsonify(dao.add_new_customer(customer))

if __name__ == "__main__":
    app.run(debug=True)




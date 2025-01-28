from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models.customers import Customer
from app.utils.decorators import login_required

customer_bp = Blueprint('customer', __name__)

# Display all customer
@customer_bp.route('/customer_list' , methods=['GET'])
@login_required
def customer_list():
    customers = Customer.get_all_customers()
    return render_template('customer_list.html', customers=customers)

# Get Customers
@customer_bp.route('/get_customers', methods=['GET'])
@login_required
def get_customers():
    customers = Customer.get_customers()
    customers_list = [{"customer_id": customer[0], "name": customer[1]} for customer in customers]
    return jsonify(customers_list)

# Add new customer
@customer_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        contact = request.form['contact']
        Customer.add_customer(name, address, contact)
        return redirect(url_for('customer.customer_list'))
    return render_template('add_customer.html')

# Edit customer
@customer_bp.route('/edit_customer/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_customer(id):
    customer = Customer.get_customer_by_id(id)
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        contact = request.form['contact']
        Customer.edit_customer(id, name, address, contact)
        return redirect(url_for('customer.customer_list'))
    return render_template('edit_customer.html', customer=customer)

# Delete customer
@customer_bp.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_customer(id):
    Customer.delete_customer(id)
    return redirect(url_for('customer.customer_list'))

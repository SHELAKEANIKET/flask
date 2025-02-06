from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models.suppliers import Supplier
from app.utils.decorators import login_required


supplier_bp = Blueprint('supplier', __name__)

# Display all suppliers
@supplier_bp.route('/supplier_list')
@login_required
def supplier_list():
    suppliers = Supplier.get_all_suppliers()
    return render_template('supplier_list.html', suppliers=suppliers)

@supplier_bp.route('/get_suppliers', methods=['GET'])
@login_required
def get_suppliers():
    suppliers = Supplier.get_suppliers()
    suppliers_list = [{"supplier_id": supplier[0], "name": supplier[1]} for supplier in suppliers]
    return jsonify(suppliers_list)

# Add new supplier
@supplier_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_supplier():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        contact = request.form['contact']
        Supplier.add_supplier(name, address, contact)
        return redirect(url_for('purchase.add_purchase'))
    return render_template('add_supplier.html')

# Edit supplier
@supplier_bp.route('/edit_supplier/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_supplier(id):
    supplier = Supplier.get_supplier_by_id(id)
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        contact = request.form['contact']
        Supplier.edit_supplier(id, name, address, contact)
        return redirect(url_for('supplier.supplier_list'))
    return render_template('edit_supplier.html', supplier=supplier)

# Delete supplier
@supplier_bp.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_supplier(id):
    Supplier.delete_supplier(id)
    return redirect(url_for('supplier.supplier_list'))

from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models.products import Product
from app.utils.decorators import login_required


product_bp = Blueprint('product', __name__)

# Display all products
@product_bp.route('/products_list')
@login_required
def product_list():
    products = Product.get_all_products()
    return render_template('product_list.html', products=products)

@product_bp.route('/products')
@login_required
def products():
    products = Product.get_products()
    return products

@product_bp.route('/get_products', methods=['GET'])
@login_required
def get_products():
    products_raw = Product.get_products()
    products = [{"product_id": product[0], "name": product[1], "type_id":product[2]} for product in products_raw]
    return jsonify(products)

@product_bp.route('/get_product_details', methods=['POST'])
@login_required
def get_product_details():
    product_name = request.json.get('product_name')

    if not product_name:
        return jsonify({"error": "Product name is required"}), 400

    # Fetch product details using the ProductModel
    product = Product.get_product_details(product_name)

    if product:
        return jsonify({"product_id": product[0], "type_id": product[1], "type_name": product[2]})
    return jsonify({"error": "Product not found"}), 404


# Add a new product
@product_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            name = data.get('name')
            type_id = data.get('type_id')
            sale_price = data.get('sale_price')
            stock_threshold = data.get('stock_threshold', 10)
            try:
                Product.add_product(name, type_id, sale_price, stock_threshold)
                # Fetch the last inserted ID
                new_product_id = Product.get_last_inserted_id()
                return jsonify({"success": True, "product_id": new_product_id, "name": name})
            except Exception as e:
                return jsonify({"success": False, "error": str(e)}), 500
        else:
            # Handle normal form submission
            name = request.form['name']
            type_id = request.form['type_id']
            sale_price = request.form['sale_price']
            stock_threshold = request.form['stock_threshold']
            Product.add_product(name, type_id, sale_price, stock_threshold)
            return redirect(url_for('product.product_list'))
    return render_template('add_product.html')

# update product 
@product_bp.route('/edit_product/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Product.get_product_by_id(id)
    if request.method == 'POST':
        name = request.form['name']
        type_id = request.form['type_id']
        sale_price = request.form['sale_price']
        stock_threshold = request.form['stock_threshold']
        Product.edit_product(id, name, type_id, sale_price, stock_threshold)
        return redirect(url_for('product.product_list'))
    return render_template('edit_product.html', product=product)

# Delete product
@product_bp.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_product(id):
    Product.delete_product(id)
    return redirect(url_for('product.product_list'))
    

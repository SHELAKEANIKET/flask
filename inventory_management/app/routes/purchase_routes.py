from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from datetime import datetime
from app.utils.db import mysql
from app.models.purchases import Purchase
from app.models.purchase_items import PurchaseItems
from app.models.suppliers import Supplier
from app.models.products import Product
from app.utils.decorators import login_required


purchase_bp = Blueprint('purchase', __name__)

# Display all purchases
@purchase_bp.route('/')
@login_required
def purchase_list():
    purchases = Purchase.get_all_purchases()
    return render_template('purchase_list.html', purchases=purchases)

# Add a new purchase
@purchase_bp.route('/add_purchase', methods=['GET', 'POST'])
@login_required
def add_purchase():
    if request.method == 'GET':
        try:
            # Fetch suppliers for the dropdown
            suppliers = Purchase.get_supplier()
            products_raw = Product.get_products()   
            products = [{"product_id": product[0], "name": product[1], "type_id":product[2]} for product in products_raw]
            return render_template('add_purchase.html', suppliers=suppliers, products=products,)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    if request.method == 'POST':
        try:
            # Process form data
            supplier_id = request.form['supplier_id']
            product_ids = request.form.getlist('product_ids[]')
            type_ids = request.form.getlist('type_ids[]')
            purchase_prices = request.form.getlist('purchase_price[]')
            quantities = request.form.getlist('quantity[]')
            weights = request.form.getlist('weight[]')
            
            # Create purchase record
            purchase_date = datetime.today().strftime('%Y-%m-%d')
            purchase_id = Purchase.create_purchase(supplier_id, purchase_date)
            
            if not (len(product_ids) == len(type_ids) == len(purchase_prices) == len(quantities) == len(weights)):
                return jsonify({"error": "Mismatched form data lengths"}), 400

            # Iterate through the products and process each one
            for i in range(len(product_ids)):
                product_id = product_ids[i]
                type_id = type_ids[i]
                purchase_price = float(purchase_prices[i])
                quantity = int(quantities[i])
                weight = float(weights[i]) if weights[i] else None

                # Check if product exists
                existing_product = Purchase.get_product_by_id(product_id)

                if not existing_product:
                    # Add a new product if it doesn't exist
                    type_id = request.form['type_id']
                    sale_price = float(request.form['sale_price'])
                    stock_threshold = int(request.form['stock_threshold'])
                    Purchase.add_new_product(
                        product_id=product_id,
                        type_id=type_id,
                        sale_price=sale_price,
                        stock_threshold=stock_threshold,
                        stock_quantity=quantity,
                        stock_weight=weight,
                    )
                    
                else:
                    # Update stock for existing product
                    Purchase.update_product_stock(
                        product_id=product_id,
                        quantity=quantity,
                    )

                # Add purchase items
                PurchaseItems.add_purchase_items(
                    purchase_id=purchase_id,
                    product_id=product_id,
                    type_id=type_id,
                    purchase_price=purchase_price,
                    quantity=quantity,
                    weight=weight,
                )

            # Commit all changes
            mysql.connection.commit()
            return redirect(url_for('purchase.purchase_list'))

        except Exception as e:
            mysql.connection.rollback()  # Rollback changes on error
            return jsonify({'error': str(e)}), 500

# Purchase details
@purchase_bp.route('/purchase_details', methods=['GET', 'POST'])
@login_required
def purchase_details():
    purchases = []
    purchase_items = []
    supplier_name = None
    purchase_date = None
    
    if request.method == "POST":
        supplier_name = request.form.get("supplier_name")
        purchase_date = request.form.get("purchase_date")

        # Get supplier ID from supplier name
        supplier = Supplier.get_supplier_id_by_name(supplier_name)
        
        if supplier:
            supplier_id = supplier[0] # Get supplier ID

            # Get purchase details
            purchases = Purchase.purchase_details(supplier_id, purchase_date)
            
            # Convert purchases to dictionaries for template rendering
            purchases = [
                {
                    "purchase_id": row[0], 
                    "supplier_name": supplier_name, 
                    "purchase_date": row[2],
                }
                for row in purchases
            ]
            
            if purchases:
                purchase_id = purchases[0]["purchase_id"]
                
                purchase_items = PurchaseItems.get_purchase_items(purchase_id)
                
                 # Convert purchase items to dictionaries
                purchase_items = [
                    {
                        "purchase_item_id": item[0],
                        "product_name": item[1],
                        "quantity": item[2],
                        "unit_price": float(item[3]),
                    }
                    for item in purchase_items
                ]
        
    return render_template(
        "purchase_list.html",
        purchases=purchases,
        supplier_name=supplier_name,
        purchase_date=purchase_date,
        purchase_items=purchase_items
    )
    

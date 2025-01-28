from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from datetime import datetime
from app.utils.db import mysql
from app.models.sales import Sale
from app.models.sale_items import SaleItems
from app.models.customers import Customer
from app.models.products import Product
from app.utils.decorators import login_required


sale_bp = Blueprint('sale', __name__)

# Display all sales
@sale_bp.route('/')
@login_required
def sale_list():
    sales = Sale.get_all_sales()
    return render_template('sale_list.html', sales=sales)

# Add a new sale
@sale_bp.route('/add_sale', methods=['GET', 'POST'])
@login_required
def add_sale():
    if request.method == 'GET':
        try:
            # Fetch customers for the dropdown
            customers = Sale.get_customer()
            products_raw = Product.get_products()   
            products = [{"product_id": product[0], "name": product[1], "type_id":product[2]} for product in products_raw]
            return render_template('add_sale.html', customers=customers, products=products)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    if request.method == 'POST':
        try:
            # Process form data
            customer_id = request.form['customer_id']
            product_ids = request.form.getlist('product_ids[]')
            type_ids = request.form.getlist('type_ids[]')
            sale_prices = request.form.getlist('sale_price[]')
            quantities = request.form.getlist('quantity[]')
            weights = request.form.getlist('weight[]')
            
            # Validate that all lists are of the same length
            if not (len(product_ids) == len(type_ids) == len(sale_prices) == len(quantities) == len(weights)):
                return jsonify({"error": "Mismatched form data lengths"}), 400
            
            # Create sale record
            sale_date = datetime.today().strftime('%Y-%m-%d')
            sale_id = Sale.create_sale(customer_id,sale_date)
            
            # Iterate through the products and process each one
            for i in range(len(product_ids)):
                product_id = product_ids[i]
                type_id = type_ids[i]
                sale_price = float(sale_prices[i])
                quantity = int(quantities[i])
                weight = float(weights[i]) if weights[i] else None
                
                Sale.update_product_stock(
                    product_id=product_id,
                    quantity=quantity,
                )
                
                SaleItems.add_sale_items(
                    sale_id=sale_id,
                    product_id=product_id,
                    type_id=type_id,
                    sale_price=sale_price,
                    quantity=quantity,
                    weight=weight,
                )
            
            # Commit all changes
            mysql.connection.commit()
            return redirect(url_for('sale.sale_list'))
                

        except Exception as e:
            mysql.connection.rollback()  # Rollback changes on error
            return jsonify({'error': str(e)}), 500

# Sale details
@sale_bp.route('/sale_details', methods=['GET', 'POST'])
@login_required
def sale_details():
    sales = []
    sale_items = []
    customer_name = None
    sale_date = None
    
    if request.method == "POST":
        customer_name = request.form.get("customer_name")
        sale_date = request.form.get("sale_date")
        
        # Get customer ID from customer name
        customer = Customer.get_customer_id_by_name(customer_name)
        
        if customer:
            customer_id = customer[0] # Get customer ID

            # Get sale details
            sales = Sale.sale_details(customer_id,sale_date)
            
             # Convert sales to dictionaries for template rendering
            sales = [
                {
                    "sale_id": row[0], 
                    "customer_name": customer_name, 
                    "sale_date": row[2]
                }
                for row in sales
            ]
        
            if sales:
                sale_id = sales[0]["sale_id"]
            
                sale_items = SaleItems.get_sale_items(sale_id)
                
                 # Convert sale items to dictionaries
                sale_items = [
                    {
                        "sale_item_id": item[0], 
                        "product_name": item[1],
                        "quantity": item[2],
                        "unit_price": float(item[3]),
                    }
                    for item in sale_items
                ]
        
    return render_template(
    "sale_list.html",
    sales=sales,
    customer_name=customer_name,
    sale_date=sale_date,
    sale_items=sale_items
    )
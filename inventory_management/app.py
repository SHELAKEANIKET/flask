from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'inventory_management'

mysql = MySQL(app)

# dashboard
@app.route('/')
def dashboard():
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM products")
    total_products = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM customers")
    total_customers = cur.fetchone()[0]

    cur.execute("SELECT * FROM products ORDER BY id DESC LIMIT 5")
    products = cur.fetchall()

    cur.execute("SELECT * FROM customers ORDER BY id DESC LIMIT 5")
    customers = cur.fetchall()

    return render_template('dashboard.html', total_products=total_products, total_customers=total_customers, products=products, customers=customers)

# ! Product =>
# add product
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        curr = mysql.connection.cursor()
        supplier = request.form['supplier']
        name = request.form['name']
        description = request.form['description']
        quantity = request.form['quantity']
        weight = request.form['weight']
        rate = request.form['rate']
        amount = request.form['amount']
        curr.execute('''INSERT INTO products (supplier, name, description, quantity, weight, rate, amount) VALUES (%s, %s, %s, %s, %s, %s, %s)''', (supplier, name, description, quantity, weight, rate, amount))
        mysql.connection.commit()
        curr.close()
    return render_template('add_product.html')

# edit product
@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    curr = mysql.connection.cursor()
    curr.execute('''SELECT * FROM products WHERE id = %s''', (id,))
    product = curr.fetchone()
    curr.close()
    if request.method == 'POST':
        supplier = request.form['supplier']
        name = request.form['name']
        description = request.form['description']
        quantity = request.form['quantity']
        weight = request.form['weight']
        rate = request.form['rate']
        amount = request.form['amount']
        curr = mysql.connection.cursor()
        curr.execute('''UPDATE products SET supplier = %s, name = %s, description = %s, quantity = %s, weight = %s, rate = %s, amount = %s WHERE id = %s''', (supplier, name, description, quantity, weight, rate, amount, id))
        mysql.connection.commit()
        curr.close()
        return redirect('/products_list')
    return render_template('edit_product.html', product=product)

# delete product
@app.route('/delete_product/<int:id>', methods=['GET', 'POST'])
def delete_product(id):
    curr = mysql.connection.cursor()
    curr.execute('''DELETE FROM products WHERE id = %s''', (id,))
    mysql.connection.commit()
    curr.close()
    return redirect('/products_list')

# view products
@app.route('/products_list', methods=['GET', 'POST'])
def view_products():
    curr = mysql.connection.cursor()
    curr.execute("SELECT id, supplier, name, description, quantity, weight, rate, amount FROM products")
    data = curr.fetchall()
    curr.close()
    return render_template('product_list.html', data=data)

# ! Customer =>
# add customer
@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        curr = mysql.connection.cursor()
        customer = request.form['customer'] # customer name
        name = request.form['name'] # product name
        quantity = request.form['quantity']
        amount = request.form['amount']
        curr.execute('''INSERT INTO customers (customer, name, quantity, amount) VALUES (%s, %s, %s, %s)''', (customer, name, quantity, amount))
        mysql.connection.commit()
        curr.close()
    return render_template('add_customer.html')

# edit customer
@app.route('/edit_customer/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    curr = mysql.connection.cursor()
    curr.execute('''SELECT * FROM customers WHERE id = %s''', (id,))
    customer = curr.fetchone()
    curr.close()
    if request.method == 'POST':
        customer = request.form['customer'] # customer name
        name = request.form['name'] # product name
        quantity = request.form['quantity']
        amount = request.form['amount']
        curr = mysql.connection.cursor()
        curr.execute('''UPDATE customers SET customer = %s, name = %s, quantity = %s, amount = %s WHERE id = %s''', (customer, name, quantity, amount, id))
        mysql.connection.commit()
        curr.close()
        return redirect('/customers_list')
    return render_template('edit_customer.html', customer=customer)

# delete product
@app.route('/delete_customer/<int:id>', methods=['GET', 'POST'])
def delete_customer(id):
    curr = mysql.connection.cursor()
    curr.execute('''DELETE FROM customers WHERE id = %s''', (id,))
    mysql.connection.commit()
    curr.close()
    return redirect('/customers_list')

# view products
@app.route('/customers_list', methods=['GET', 'POST'])
def view_customers():
    curr = mysql.connection.cursor()
    curr.execute("SELECT id, customer, name, quantity, amount FROM customers")
    data = curr.fetchall()
    curr.close()
    return render_template('customer_list.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)
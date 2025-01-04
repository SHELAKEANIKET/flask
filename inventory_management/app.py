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
    return render_template('dashboard.html')

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
    data = curr.fetchall()
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
    return render_template('edit_product.html', data=data)

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
    curr.execute('''SELECT * FROM products''')
    data = curr.fetchall()
    curr.close()
    return render_template('product_list.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)
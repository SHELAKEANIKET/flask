from app.utils.db import mysql

class Product:
    @staticmethod
    def get_all_products():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM products")
        products = cur.fetchall()
        cur.close()
        return products

    @staticmethod
    def get_products():
        cur = mysql.connection.cursor()
        query = "SELECT product_id, name, type_id FROM products"
        cur.execute(query)
        products = cur.fetchall()
        cur.close()
        return products

    @staticmethod
    def get_product_by_id(id):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM products WHERE product_id = %s", (id,))
        product = cur.fetchone()
        cur.close()
        return product
    
    @staticmethod
    def get_last_inserted_id():
        cur = mysql.connection.cursor()
        cur.execute("SELECT LAST_INSERT_ID()")
        last_inserted_id = cur.fetchone()
        cur.close()
        return last_inserted_id
    
    @staticmethod
    def get_product_details(product_name):
        cur = mysql.connection.cursor()
        query = "SELECT p.product_id, p.type_id, t.type_name FROM products p JOIN types t ON p.type_id = t.type_id WHERE p.name = %s"
        cur.execute(query, (product_name,))
        product = cur.fetchone()
        cur.close()
        return product

    @staticmethod
    def add_product(name, type_id, sale_price, stock_threshold):
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO products (name, type_id, sale_price, stock_threshold)
            VALUES (%s, %s, %s, %s)
        """, (name, type_id, sale_price, stock_threshold))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def edit_product(id, name, type_id, sale_price, stock_threshold):
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE products
            SET name = %s, type_id = %s, sale_price = %s, stock_threshold = %s
            WHERE product_id = %s
        """, (name, type_id, sale_price, stock_threshold, id))
        mysql.connection.commit()
        cur.close()
        
    @staticmethod
    def delete_product(id):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM products WHERE product_id = %s", (id,))
        mysql.connection.commit()
        cur.close()

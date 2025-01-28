from app.utils.db import mysql

class Purchase:
   @staticmethod
   def get_all_purchases():
         cur = mysql.connection.cursor()
         cur.execute("SELECT * FROM purchases")
         purchases = cur.fetchall()
         cur.close()
         return purchases
   
   @staticmethod
   def get_supplier():
        cur = mysql.connection.cursor()
        cur.execute("SELECT supplier_id, name FROM suppliers")
        suppliers = cur.fetchall()
        cur.close()
        return suppliers
   
   @staticmethod
   def create_purchase(supplier_id,purchase_date):   
        cur = mysql.connection.cursor()
        query = "INSERT INTO purchases (supplier_id, purchase_date) VALUES (%s, %s)"
        cur.execute(query, (supplier_id, purchase_date))
        mysql.connection.commit()
        purchase_id = cur.lastrowid
        cur.close()
        return purchase_id
   
   @staticmethod
   def get_product_by_id(product_id):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
        product = cur.fetchone()
        cur.close()
        return product
   
   @staticmethod
   def add_new_product(product_id, type_id, sale_price, stock_threshold, stock_quantity, stock_weight):
        cur = mysql.connection.cursor()
        cur.execute(
            """
            INSERT INTO products (product_id, type_id, sale_price, stock_threshold, stock_quantity, stock_weight)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (product_id, type_id, sale_price, stock_threshold, stock_quantity, stock_weight),
        )
        cur.close()
        
   @staticmethod
   def update_product_stock(product_id, quantity):
        cur = mysql.connection.cursor()
        cur.execute(
            """
            UPDATE products
            SET stock_quantity = stock_quantity + %s,
            WHERE product_id = %s
            """,
            (quantity, product_id),
        )
        cur.close()
        
   @staticmethod    
   def purchase_details(supplier_id, purchase_date):
        cur = mysql.connection.cursor()
        cur.execute("""
                    SELECT purchase_id, supplier_id, DATE(purchase_date) as purchase_date
                    FROM purchases 
                    WHERE supplier_id = %s AND DATE(purchase_date) = %s
                    """,
                    (supplier_id, purchase_date)
               )
        purchases = cur.fetchall()
        cur.close()
        return purchases

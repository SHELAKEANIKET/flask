from app.utils.db import mysql

class Sale:
    @staticmethod
    def get_all_sales():
         cur = mysql.connection.cursor()
         cur.execute("SELECT * FROM sales")
         sales = cur.fetchall()
         cur.close()
         return sales
     
    @staticmethod
    def get_customer():
         cur = mysql.connection.cursor()
         cur.execute("SELECT customer_id, name FROM customers")
         customers = cur.fetchall()
         cur.close()
         return customers
    
    @staticmethod
    def create_sale(customer_id,sale_date):
         cur = mysql.connection.cursor()
         query = "INSERT INTO sales (customer_id, sale_date) VALUES (%s, %s)"
         cur.execute(query, (customer_id, sale_date))
         mysql.connection.commit()
         sale_id = cur.lastrowid
         cur.close()
         return sale_id
     
    @staticmethod
    def get_product_by_id(product_id):
         cur = mysql.connection.cursor()
         cur.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
         product = cur.fetchone()
         cur.close()
         return product
     
    @staticmethod
    def update_product_stock(product_id, quantity):
         cur = mysql.connection.cursor()
         cur.execute(
             """
             UPDATE products
             SET stock_quantity = stock_quantity - %s,
             WHERE product_id = %s
             """,
             (quantity, product_id),
         )
         cur.close()
         
         
    @staticmethod    
    def sale_details(customer_id, sale_date):
        cur = mysql.connection.cursor()
        cur.execute("""
                    SELECT sale_id, customer_id, DATE(sale_date) as sale_date
                    FROM sales 
                    WHERE customer_id = %s AND DATE(sale_date) = %s
                    """,
                    (customer_id, sale_date)
               )
        sales = cur.fetchall()
        cur.close()
        return sales
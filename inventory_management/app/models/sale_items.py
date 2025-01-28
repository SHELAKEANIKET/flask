from app.utils.db import mysql

class SaleItems:
    @staticmethod
    def add_sale_items(sale_id, product_id, type_id, sale_price, quantity, weight):
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO sale_items (sale_id, product_id, type_id, sale_price, quantity, weight)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (sale_id, product_id, type_id, sale_price, quantity, weight))
                      
        mysql.connection.commit()
        cur.close()
        
    @staticmethod
    def get_sale_items(sale_id):
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT pi.sale_item_id, p.name AS product_name, pi.quantity, pi.sale_price FROM sale_items pi
            JOIN products p ON pi.product_id = p.product_id
            WHERE pi.sale_id = %s
        """, (sale_id,))
        sale_items = cur.fetchall()
        cur.close()
        return sale_items
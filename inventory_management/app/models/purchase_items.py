from app.utils.db import mysql

class PurchaseItems:
    @staticmethod
    def add_purchase_items(purchase_id, product_id, type_id, purchase_price, quantity, weight):
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO purchase_items (purchase_id, product_id, type_id, purchase_price, quantity, weight)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (purchase_id, product_id, type_id, purchase_price, quantity, weight))
                      
        mysql.connection.commit()
        cur.close()
    
    @staticmethod
    def get_purchase_items(purchase_id):
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT pi.purchase_item_id, p.name AS product_name, pi.quantity, pi.purchase_price FROM purchase_items pi
            JOIN products p ON pi.product_id = p.product_id
            WHERE pi.purchase_id = %s
        """, (purchase_id,))
        purchase_items = cur.fetchall()
        cur.close()
        return purchase_items
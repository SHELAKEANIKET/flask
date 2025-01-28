from app.utils.db import mysql

class Dashboard:
    @staticmethod
    def get_total_customers():
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*) FROM customers")
        total_customers = cur.fetchone()[0]
        cur.close()
        return total_customers
    
    @staticmethod
    def get_total_products():
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*) FROM products")
        total_products = cur.fetchone()[0]
        cur.close()
        return total_products
    
    @staticmethod
    def get_total_suppliers():
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*) FROM suppliers")
        total_suppliers = cur.fetchone()[0]
        cur.close()
        return total_suppliers
    
    @staticmethod
    def get_total_sales():
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*) FROM sales")
        total_sales = cur.fetchone()[0]
        cur.close()
        return total_sales
    
    @staticmethod
    def get_total_purchases():
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*) FROM purchases")
        total_purchases = cur.fetchone()[0]
        cur.close()
        return total_purchases
    
    # @staticmethod
    # def get_total_revenue():
    #     cur = mysql.connection.cursor()
    #     cur.execute("SELECT SUM(total_price) FROM sales")
    #     total_revenue = cur.fetchone()[0]
    #     cur.close()
    #     return total_revenue
    
    # @staticmethod
    # def get_total_cost():
    #     cur = mysql.connection.cursor()
    #     cur.execute("SELECT SUM(total_price) FROM purchases")
    #     total_cost = cur.fetchone()[0]
    #     cur.close()
    #     return total_cost
    
    @staticmethod
    def get_total_profit():
        total_revenue = Dashboard.get_total_revenue()
        total_cost = Dashboard.get_total_cost()
        total_profit = total_revenue - total_cost
        return total_profit
    
    @staticmethod
    def get_total_stock():
        cur = mysql.connection.cursor()
        cur.execute("SELECT SUM(stock_quantity) FROM products")
        total_stock = cur.fetchone()[0]
        cur.close()
        return total_stock
    
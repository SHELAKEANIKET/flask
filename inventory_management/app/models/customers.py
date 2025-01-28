from app.utils.db import mysql

class Customer:
    @staticmethod
    def get_all_customers():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM customers")
        customers = cur.fetchall()
        cur.close()
        return customers
    
    @staticmethod
    def get_customers():
        cur = mysql.connection.cursor()
        cur.execute("SELECT customer_id, name FROM customers")
        customers = cur.fetchall()
        cur.close()
        return customers
    
    @staticmethod
    def get_customer_by_id(id):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM customers WHERE customer_id = %s", (id,))
        customer = cur.fetchone()
        cur.close()
        return customer
    
    @staticmethod
    def get_customer_id_by_name(customer_name):
        cur = mysql.connection.cursor()
        cur.execute("SELECT customer_id FROM customers WHERE name = %s", (customer_name,))
        customer = cur.fetchone()
        cur.close()
        return customer

    @staticmethod
    def add_customer(name, address, contact):
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO customers (name, address, contact)
            VALUES (%s, %s, %s)
        """, (name, address, contact))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def edit_customer(id, name, address, contact):
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE customers
            SET name = %s, address = %s, contact = %s
            WHERE customer_id = %s
        """, (name, address, contact, id))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def delete_customer(id):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM customers WHERE customer_id = %s", (id,))
        mysql.connection.commit()
        cur.close()
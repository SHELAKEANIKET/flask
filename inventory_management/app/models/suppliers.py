from app.utils.db import mysql

class Supplier:
    @staticmethod
    def get_all_suppliers():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM suppliers")
        suppliers = cur.fetchall()
        cur.close()
        return suppliers
    
    @staticmethod
    def get_suppliers():
        cur = mysql.connection.cursor()
        cur.execute("SELECT supplier_id, name FROM suppliers")
        suppliers = cur.fetchall()
        cur.close()
        return suppliers
    
    @staticmethod
    def get_supplier_by_name(name):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM suppliers WHERE name = %s", (name,))
        supplier = cur.fetchone()
        cur.close()
        return supplier
    
    @staticmethod
    def get_supplier_by_id(id):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM suppliers WHERE supplier_id = %s", (id,))
        supplier = cur.fetchone()
        cur.close()
        return supplier
    
    @staticmethod
    def get_supplier_id_by_name(supplier_name):
        cur = mysql.connection.cursor()
        cur.execute("SELECT supplier_id FROM suppliers WHERE name = %s", (supplier_name,))
        supplier = cur.fetchone()
        cur.close()
        return supplier

    @staticmethod
    def add_supplier(name, address, contact):   
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO suppliers (name, address, contact)
            VALUES (%s, %s, %s)
        """, (name, address, contact))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def edit_supplier(id, name, address, contact):
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE suppliers
            SET name = %s, address = %s, contact = %s
            WHERE supplier_id = %s
        """, (name, address, contact, id))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def delete_supplier(id):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM suppliers WHERE supplier_id = %s", (id,))
        mysql.connection.commit()
        cur.close()
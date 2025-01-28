from app.utils.db import mysql

class Type:
    @staticmethod
    def get_all_types():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM types")
        types = cur.fetchall()
        cur.close()
        return types
    
    @staticmethod
    def get_types():
        cur = mysql.connection.cursor()
        cur.execute("SELECT type_id, type_name FROM types")
        types = cur.fetchall()
        cur.close()
        return types
    
    @staticmethod
    def get_type_by_id(id):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM types WHERE type_id = %s", (id,))
        type = cur.fetchone()
        cur.close()
        return type
    
    @staticmethod
    def add_type(type_name, parent_product_id=None):
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO types (type_name, parent_product_id)
            VALUES (%s, %s)
        """, (type_name, parent_product_id))
        mysql.connection.commit()
        cur.close()
        
    @staticmethod
    def edit_type(type_id, type_name, parent_product_id=None):
        cur = mysql.connection.cursor()
        cur.execute(
            """
            UPDATE types
            SET type_name = %s, parent_product_id = %s
            WHERE type_id = %s
            """, (type_name, parent_product_id, type_id))
        mysql.connection.commit()   
        cur.close()
        
    @staticmethod   
    def delete_type(type_id):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM types WHERE type_id = %s", (type_id,))
        mysql.connection.commit()
        cur.close() 
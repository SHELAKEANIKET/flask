from flask import Flask
from app.utils.db import init_db
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'inventory_management'
    
    app.secret_key = os.getenv("SECRET_KEY")

    init_db(app)
    Bcrypt(app)

    
    # dashboard route
    from app.routes.dashboard_routes import dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix='/')

    # product routes
    from app.routes.product_routes import product_bp
    app.register_blueprint(product_bp, url_prefix='/products')
    
    # customer routes
    from app.routes.customer_routes import customer_bp
    app.register_blueprint(customer_bp, url_prefix='/customers')
    
    # supplier routes
    from app.routes.supplier_routes import supplier_bp
    app.register_blueprint(supplier_bp, url_prefix='/suppliers')
    
    # purchase routes
    from app.routes.purchase_routes import purchase_bp
    app.register_blueprint(purchase_bp, url_prefix='/purchases')
    
    # sale routes
    from app.routes.sale_routes import sale_bp
    app.register_blueprint(sale_bp, url_prefix='/sales')
    
    # type routes
    from app.routes.type_routes import type_bp
    app.register_blueprint(type_bp, url_prefix='/types')
    
    from app.routes.admin_routes import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app

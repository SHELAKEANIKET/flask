from flask import Blueprint, render_template
from app.models.dashboard import Dashboard
from app.utils.decorators import login_required

dashboard_bp = Blueprint('dashboard', __name__)

# Display dashboard
@dashboard_bp.route('/')
@login_required
def dashboard():
    total_customers = Dashboard.get_total_customers()
    total_products = Dashboard.get_total_products()
    total_suppliers = Dashboard.get_total_suppliers()
    total_sales = Dashboard.get_total_sales()
    total_purchases = Dashboard.get_total_purchases()
    # total_revenue = Dashboard.get_total_revenue()
    # total_cost = Dashboard.get_total_cost()
    return render_template('dashboard.html', total_customers=total_customers, total_products=total_products, total_suppliers=total_suppliers, total_sales=total_sales, total_purchases=total_purchases,)
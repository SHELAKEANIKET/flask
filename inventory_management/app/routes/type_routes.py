from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from datetime import datetime
from app.utils.db import mysql
from app.models.types import Type
from app.utils.decorators import login_required


type_bp = Blueprint('type', __name__)

# get all types
@type_bp.route('/type_list', methods=['GET'])
@login_required
def get_all_types():
    types = Type.get_all_types()
    return render_template('type_list.html', types=types)

# get types
@type_bp.route('/get_types', methods=['GET'])
@login_required
def get_types():
    types = Type.get_types()
    types_list = [{"type_id": type[0], "type_name": type[1]} for type in types]
    return jsonify(types_list)

# add new type
@type_bp.route('/add_type', methods=['GET', 'POST'])
@login_required
def add_type():
    if request.method == 'POST':
        type_name = request.form['type_name']
        parent_product_id = request.form.get('parent_product_id')  # Optional field
        Type.add_type(type_name, parent_product_id)
        return redirect(url_for('type.type_list'))
    return render_template('add_type.html')

# update a type
@type_bp.route('/edit_type/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_type(id):
    type = Type.get_type_by_id(id)
    if request.method == 'POST':
        name = request.form['type_name']
        parent_product_id = request.form.get('parent_product_id')
   
        Type.edit_type(id, name, parent_product_id)
        return redirect(url_for('type.type_list'))
    return render_template('edit_type.html', type=type)

# delete a type
@type_bp.route('/delete_type/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_type(id):
    Type = Type.delete_type(id)
    return redirect(url_for('type.type_list'))
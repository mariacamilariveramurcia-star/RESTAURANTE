from flask import Blueprint, render_template

# Se define el Blueprint con el prefijo /admin
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/')
def admin():
    return render_template('admin.html')

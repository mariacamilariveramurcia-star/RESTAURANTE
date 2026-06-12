from flask import Blueprint, request, jsonify
from models import db, Dish, Order, Review

# Se define el Blueprint con el prefijo /api
api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/admin/pedidos')
def api_admin_pedidos():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return jsonify([{
        'id':         o.id,
        'name':       o.name,
        'phone':      o.phone,
        'email':      o.email or '',
        'address':    o.address or '',
        'tipo':       o.tipo,
        'notes':      o.notes or '',
        'total':      o.total,
        'status':     o.status,
        'created_at': o.created_at.strftime('%d/%m/%Y %H:%M'),
        'items': [{
            'dish_name': i.dish_name,
            'quantity':  i.quantity,
            'price':     i.price
        } for i in o.items]
    } for o in orders])


@api_bp.route('/admin/pedidos/<int:id>', methods=['PATCH'])
def api_update_pedido(id):
    data = request.get_json()
    o = Order.query.get_or_404(id)
    o.status = data.get('status', o.status)
    db.session.commit()
    return jsonify({'success': True})


@api_bp.route('/review', methods=['POST'])
def add_review():
    data = request.get_json()
    db.session.add(Review(
        name    = data.get('name', 'Anónimo'),
        rating  = int(data.get('rating', 5)),
        comment = data.get('comment', '')))
    db.session.commit()
    return jsonify({'success': True})


@api_bp.route('/dishes')
def api_dishes():
    dishes = Dish.query.filter_by(is_available=True).all()
    return jsonify([{
        'id':          d.id,
        'name':        d.name,
        'name_jp':     d.name_jp,
        'price':       d.price,
        'category':    d.category.name,
        'image_url':   d.image_url,
        'spice_level': d.spice_level,
        'is_featured': d.is_featured
    } for d in dishes])

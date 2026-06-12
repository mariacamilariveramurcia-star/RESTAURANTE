from flask import Blueprint, render_template, request, jsonify
from models import db, Dish, Category, Review, Order, OrderItem

# Se define el Blueprint con su nombre
paginas_bp = Blueprint('paginas', __name__)


@paginas_bp.route('/')
def index():
    featured   = Dish.query.filter_by(is_featured=True, is_available=True).all()
    reviews    = Review.query.filter_by(approved=True).order_by(Review.created_at.desc()).limit(4).all()
    categories = Category.query.all()
    return render_template('index.html', featured=featured, reviews=reviews, categories=categories)


@paginas_bp.route('/menu')
def menu():
    categories = Category.query.all()
    all_prices = [d.price for d in Dish.query.filter_by(is_available=True).all()]
    global_min = int(min(all_prices)) if all_prices else 0
    global_max = int(max(all_prices)) if all_prices else 100000

    selected_cat = request.args.get('categoria', type=int)
    precio_min   = request.args.get('precio_min', type=float)
    precio_max   = request.args.get('precio_max', type=float)
    spice_raw    = request.args.get('picante', '')
    spice        = int(spice_raw) if spice_raw.isdigit() else None
    solo_dest    = request.args.get('destacados') == '1'
    orden        = request.args.get('orden', 'default')

    q = Dish.query.filter_by(is_available=True)
    if selected_cat:             q = q.filter_by(category_id=selected_cat)
    if precio_min is not None:   q = q.filter(Dish.price >= precio_min)
    if precio_max is not None:   q = q.filter(Dish.price <= precio_max)
    if spice is not None:        q = q.filter(Dish.spice_level == spice)
    if solo_dest:                q = q.filter_by(is_featured=True)
    if orden == 'precio_asc':    q = q.order_by(Dish.price.asc())
    elif orden == 'precio_desc': q = q.order_by(Dish.price.desc())
    elif orden == 'nombre':      q = q.order_by(Dish.name.asc())

    return render_template('menu.html',
        categories=categories, dishes=q.all(),
        selected_cat=selected_cat,
        precio_min=precio_min, precio_max=precio_max,
        spice=spice, solo_dest=solo_dest, orden=orden,
        global_min=global_min, global_max=global_max)


@paginas_bp.route('/dish/<int:id>')
def dish_detail(id):
    dish    = Dish.query.get_or_404(id)
    related = Dish.query.filter_by(category_id=dish.category_id, is_available=True)\
                        .filter(Dish.id != id).limit(3).all()
    return render_template('dish_detail.html', dish=dish, related=related)


@paginas_bp.route('/pedidos', methods=['GET', 'POST'])
def pedidos():
    categories = Category.query.all()
    dishes     = Dish.query.filter_by(is_available=True).all()
    if request.method == 'POST':
        data  = request.get_json()
        items = data.get('items', [])
        if not items:
            return jsonify({'success': False, 'msg': 'El carrito está vacío'})
        total = sum(i['price'] * i['quantity'] for i in items)
        order = Order(
            name    = data.get('name', ''),
            phone   = data.get('phone', ''),
            email   = data.get('email', ''),
            address = data.get('address', ''),
            tipo    = data.get('tipo', 'recoger'),
            notes   = data.get('notes', ''),
            total   = total
        )
        db.session.add(order)
        db.session.flush()
        for i in items:
            db.session.add(OrderItem(
                order_id  = order.id,
                dish_id   = i['dish_id'],
                dish_name = i['name'],
                quantity  = i['quantity'],
                price     = i['price']
            ))
        db.session.commit()
        return jsonify({'success': True, 'order_id': order.id})
    return render_template('pedidos.html', categories=categories, dishes=dishes)

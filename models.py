from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ─── Modelos ───────────────────────────────────────────────────────────────

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    name_jp = db.Column(db.String(100))
    icon = db.Column(db.String(10))
    dishes = db.relationship('Dish', backref='category', lazy=True)

class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    name_jp = db.Column(db.String(150))
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(300))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    is_featured = db.Column(db.Boolean, default=False)
    is_available = db.Column(db.Boolean, default=True)
    spice_level = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(150))
    address = db.Column(db.String(300))
    tipo = db.Column(db.String(20), default='recoger')  # recoger / domicilio
    notes = db.Column(db.Text)
    total = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='nuevo')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False)
    dish_name = db.Column(db.String(150))
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Float)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved = db.Column(db.Boolean, default=True)

# ─── Seed ──────────────────────────────────────────────────────────────────

def seed_data():
    if Category.query.count() > 0:
        return
    cats = [
        Category(name='Sushi & Rolls', name_jp='寿司',    icon='🍣'),
        Category(name='Ramen',         name_jp='ラーメン', icon='🍜'),
        Category(name='Tempura',       name_jp='天ぷら',   icon='🍤'),
        Category(name='Gyoza',         name_jp='餃子',     icon='🥟'),
        Category(name='Postres',       name_jp='デザート', icon='🍡'),
    ]
    for c in cats: db.session.add(c)
    db.session.flush()

    dishes = [
        Dish(name='Dragon Roll', name_jp='ドラゴンロール',
             description='Camarón tempura, aguacate, pepino, cubierto con láminas de aguacate fresco y salsa eel.',
             price=18900, image_url='/static/images/dragon roll.png',
             category_id=cats[0].id, is_featured=True),
        Dish(name='Nigiri Salmón', name_jp='サーモン握り',
             description='Delicadas piezas de salmón fresco sobre arroz sazonado con vinagre de arroz.',
             price=12500, image_url='https://images.unsplash.com/photo-1553621042-f6e147245754?auto=format&fit=crop&w=600&q=80',
             category_id=cats[0].id, is_featured=True),
        Dish(name='Rainbow Roll', name_jp='レインボーロール',
             description='California roll cubierto con atún, salmón, aguacate y camarón.',
             price=21500, image_url='https://images.unsplash.com/photo-1562802378-063ec186a863?auto=format&fit=crop&w=600&q=80',
             category_id=cats[0].id),
        Dish(name='Spicy Tuna Roll', name_jp='スパイシーツナ',
             description='Atún fresco, pepino crujiente, cebolla verde y salsa sriracha casera.',
             price=16800, image_url='/static/images/Spicy Tuna Roll.png',
             category_id=cats[0].id, spice_level=2),
        Dish(name='Tonkotsu Ramen', name_jp='豚骨ラーメン',
             description='Caldo cremoso de huesos de cerdo 12 horas, chashu, huevo marinado, nori y cebollín.',
             price=23800, image_url='https://images.unsplash.com/photo-1569050467447-ce54b3bbc37d?auto=format&fit=crop&w=600&q=80',
             category_id=cats[1].id, is_featured=True),
        Dish(name='Shoyu Ramen', name_jp='醤油ラーメン',
             description='Caldo transparente de soya con pollo, bambú, naruto y aceite de sésamo.',
             price=20500, image_url='https://images.unsplash.com/photo-1557872943-16a5ac26437e?auto=format&fit=crop&w=600&q=80',
             category_id=cats[1].id),
        Dish(name='Spicy Miso Ramen', name_jp='辛味噌ラーメン',
             description='Caldo de miso picante, maíz dulce, mantequilla, carne molida y jengibre.',
             price=22000, image_url='https://images.unsplash.com/photo-1591814468924-caf88d1232e1?auto=format&fit=crop&w=600&q=80',
             category_id=cats[1].id, spice_level=3),
        Dish(name='Tempura Mixta', name_jp='天ぷら盛り合わせ',
             description='Camarón, vegetales de temporada y hongos shiitake en masa tempura dorada.',
             price=19200, image_url='/static/images/tempura mixta.png',
             category_id=cats[2].id, is_featured=True),
        Dish(name='Ebi Tempura', name_jp='海老天ぷら',
             description='Camarones tigre jumbo en tempura crujiente con salsa tentsuyu y daikon.',
             price=24500, image_url='/static/images/ebi tempura.png',
             category_id=cats[2].id),
        Dish(name='Gyoza de Cerdo', name_jp='豚餃子',
             description='Dumplings artesanales de cerdo y col, dorados al wok con salsa ponzu.',
             price=14500, image_url='https://images.unsplash.com/photo-1496116218417-1a781b1c416c?auto=format&fit=crop&w=600&q=80',
             category_id=cats[3].id),
        Dish(name='Edamame', name_jp='枝豆',
             description='Vainas de soya tierna con sal marina gruesa y toque de yuzu.',
             price=8900, image_url='/static/images/edamame.png',
             category_id=cats[3].id),
        Dish(name='Mochi Ice Cream', name_jp='もちアイス',
             description='Mochi artesanal relleno de helado: matcha, fresa y vainilla de Madagascar.',
             price=11500, image_url='https://images.unsplash.com/photo-1563805042-7684c019e1cb?auto=format&fit=crop&w=600&q=80',
             category_id=cats[4].id, is_featured=True),
        Dish(name='Dorayaki', name_jp='どら焼き',
             description='Panquecas esponjosas japonesas rellenas de pasta de frijol dulce anko.',
             price=9800, image_url='https://images.unsplash.com/photo-1607301406259-dfb186e15de8?auto=format&fit=crop&w=600&q=80',
             category_id=cats[4].id),
    ]
    for d in dishes: db.session.add(d)

    for r in [
        Review(name='María C.', rating=5, comment='El Tonkotsu Ramen es sublime. El caldo tiene una profundidad increíble.'),
        Review(name='Carlos R.', rating=5, comment='Dragon Roll espectacular. El ambiente es perfecto para una cena especial.'),
        Review(name='Valentina M.', rating=4, comment='La tempura mixta, crujiente y ligera. El servicio fue muy atento.'),
        Review(name='Andrés P.', rating=5, comment='El mejor japonés de la ciudad. El Rainbow Roll siempre supera mis expectativas.'),
    ]: db.session.add(r)

    db.session.commit()
    print("✅ BD inicializada.")

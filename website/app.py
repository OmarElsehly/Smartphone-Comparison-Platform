
import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.abspath(os.path.dirname(__file__)))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{basedir}/FinalPhonesDataBase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_link = db.Column(db.Text, nullable=True)
    model_name = db.Column(db.Text, nullable=False)

class Brand(db.Model):
    brand_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.Text, nullable=True)
    web_store = db.Column(db.Text, nullable=True)

class Price(db.Model):
    price_id = db.Column(db.Integer, primary_key=True)
    price_before_promotion = db.Column(db.Text, nullable=True)
    price_after_promotion = db.Column(db.Text, nullable=True)
    promotion = db.Column(db.Text, nullable=True)
    savings = db.Column(db.Text, nullable=True)

class Details(db.Model):
    details_id = db.Column(db.Integer, primary_key=True)
    colour_name = db.Column(db.Text, nullable=True)
    screen_size = db.Column(db.Text, nullable=True)
    internal_memory = db.Column(db.Text, nullable=True)
    ram_size = db.Column(db.Text, nullable=True)

class Rating(db.Model):
    ratings_id = db.Column(db.Integer, primary_key=True)
    ratings = db.Column(db.Text, nullable=True)

@app.route('/')
def index():
    phones = Info.query.all()
    return render_template('index.html', phones=phones)

@app.route('/phone/<int:phone_id>')
def phone_detail(phone_id):
    phone = Info.query.get_or_404(phone_id)
    details = Details.query.filter_by(details_id=phone.id).first()
    price = Price.query.filter_by(price_id=phone.id).first()
    brand = Brand.query.filter_by(brand_id=phone.id).first()
    rating = Rating.query.filter_by(ratings_id=phone.id).first()
    return render_template(
        'phone_detail.html',
        phone=phone,
        details=details,
        price=price,
        brand=brand,
        rating=rating,
    )
    
@app.route('/search')
def search():
    query = request.args.get('query')
    phones = Info.query.filter(Info.model_name.ilike(f'%{query}%')).all()

    results = []
    for phone in phones:
        brand = Brand.query.filter_by(brand_id=phone.id).first()
        price = Price.query.filter_by(price_id=phone.id).first()

        results.append({
            "id": phone.id,
            "model_name": phone.model_name,
            "image_link": phone.image_link,
            "company_name": brand.company_name if brand else None,
            "web_store": brand.web_store if brand else None,
            "price_after_promotion": price.price_after_promotion if price else None,
        })

    return jsonify(results)
@app.route('/filter')
def filter():
    brand = request.args.get('brand', '').strip()
    webstore = request.args.get('webstore', '').strip()
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)

    phones = Info.query.join(Brand, Info.id == Brand.brand_id).join(Price, Info.id == Price.price_id)

    if brand:
        phones = phones.filter(Brand.company_name.ilike(f'%{brand}%'))
    if webstore:
        phones = phones.filter(Brand.web_store.ilike(f'%{webstore}%'))
    if min_price is not None:
        phones = phones.filter(Price.price_after_promotion >= min_price)
    if max_price is not None:
        phones = phones.filter(Price.price_after_promotion <= max_price)

    results = []
    for phone in phones.all():
        brand = Brand.query.filter_by(brand_id=phone.id).first()
        price = Price.query.filter_by(price_id=phone.id).first()

        results.append({
            "id": phone.id,
            "model_name": phone.model_name,
            "image_link": phone.image_link,
            "company_name": brand.company_name if brand else None,
            "web_store": brand.web_store if brand else None,
            "price_after_promotion": price.price_after_promotion if price else None,
        })

    return jsonify(results)




if __name__ == '__main__':
    app.run(debug=True)
    print(basedir) 
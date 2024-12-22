
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
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

if __name__ == '__main__':
    app.run(debug=True)

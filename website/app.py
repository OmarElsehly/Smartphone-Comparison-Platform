import os
from flask import Flask, render_template, request, jsonify, session, make_response
from weasyprint import HTML, CSS
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



compare_list = []  # List to store selected phone IDs for comparison
cart = []  # Global cart list to store phone IDs

@app.route('/cart', methods=['GET'])
def view_cart():
    # Combine functionality for viewing the cart
    if 'cart' not in session or not session['cart']:
        return render_template('cart.html', phones=[], total_price=0)

    phone_ids = [int(phone_id) for phone_id in session['cart']]
    phones = Info.query.filter(Info.id.in_(phone_ids)).all()

    phone_details = []
    total_price = 0

    for phone in phones:
        price = Price.query.filter_by(price_id=phone.id).first()
        brand = Brand.query.filter_by(brand_id=phone.id).first()

        if price and price.price_after_promotion:
            phone_price = float(price.price_after_promotion)
            if brand and brand.web_store.lower() == "ebay":
                phone_price *= 50  # Convert USD to EGP for eBay
                currency = "EGP"
            else:
                currency = "EGP"
        else:
            phone_price = 0
            currency = "EGP"

        total_price += phone_price

        phone_details.append({
            'id': phone.id,
            'model_name': phone.model_name,
            'image_link': phone.image_link,
            'price_after_promotion': phone_price,
            'currency': currency,
        })

    return render_template('cart.html', phones=phone_details, total_price=total_price)


@app.route('/compare', methods=['GET'])
def compare_phones():
    if 'compare_list' not in session or len(session['compare_list']) == 0:
        return render_template('compare.html', phone_details=[])

    phone_ids = session['compare_list']
    phones = Info.query.filter(Info.id.in_(phone_ids)).all()

    phone_details = []
    for phone in phones:
        details = Details.query.filter_by(details_id=phone.id).first()
        price = Price.query.filter_by(price_id=phone.id).first()
        brand = Brand.query.filter_by(brand_id=phone.id).first()
        rating = Rating.query.filter_by(ratings_id=phone.id).first()

        phone_details.append({
            'phone': phone,
            'details': details,
            'price': price,
            'brand': brand,
            'rating': rating
        })

    return render_template('compare.html', phone_details=phone_details)



@app.route('/update_cart', methods=['POST'])
def update_cart():
    data = request.json
    phone_id = data.get('phone_id')
    action = data.get('action')

    if not phone_id:
        return jsonify({'error': 'Phone ID is required'}), 400

    # Initialize cart in session if not already
    if 'cart' not in session:
        session['cart'] = []

    cart = session['cart']

    if action == 'add':
        if phone_id not in cart:
            cart.append(phone_id)
    elif action == 'remove':
        if phone_id in cart:
            cart.remove(phone_id)
    else:
        return jsonify({'error': 'Invalid action'}), 400

    # Update the session cart
    session['cart'] = cart
    session.modified = True  # Ensure changes are saved

    return jsonify({'success': True, 'cart': cart})


@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    data = request.json
    phone_id = data.get('phone_id')

    if not phone_id:
        return jsonify({'error': 'Phone ID is required'}), 400

    # Ensure cart exists in session
    if 'cart' not in session:
        session['cart'] = []

    cart = session['cart']

    if phone_id in cart:
        cart.remove(phone_id)
        session['cart'] = cart
        session.modified = True
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Phone not found in cart'}), 400

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

@app.route('/export_comparison', methods=['GET'])
def export_comparison():
    # Check if compare list exists in the session
    if 'compare_list' not in session or len(session['compare_list']) == 0:
        return "No phones selected for comparison.", 400

    # Retrieve the phone details for the comparison
    phone_ids = session['compare_list']
    phones = Info.query.filter(Info.id.in_(phone_ids)).all()
    phone_details = []
    for phone in phones:
        details = Details.query.filter_by(details_id=phone.id).first()
        price = Price.query.filter_by(price_id=phone.id).first()
        brand = Brand.query.filter_by(brand_id=phone.id).first()
        rating = Rating.query.filter_by(ratings_id=phone.id).first()
        phone_details.append({
            'phone': phone,
            'details': details,
            'price': price,
            'brand': brand,
            'rating': rating
        })

    # Render the compare template into HTML
    html_content = render_template('compare.html', phone_details=phone_details, for_pdf=True)

    # Dynamically resolve the path for the CSS file
    css_path = os.path.join(basedir, 'static', 'pdf_styles.css')
    print(f"Using CSS file: {css_path}")  # Debug statement

    # Load the dedicated PDF CSS
    try:
        pdf_css = CSS(filename=css_path)
    except FileNotFoundError:
        return "CSS file not found. Please ensure the static/pdf_styles.css file exists.", 500

    # Generate the PDF using WeasyPrint with the custom CSS
    pdf = HTML(string=html_content).write_pdf(stylesheets=[pdf_css])

    # Serve the PDF as a downloadable file
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=comparison.pdf'
    return response


@app.route('/compare')
def compare():
    # Retrieve the phone IDs from the session compare list
    if 'compare_list' not in session or len(session['compare_list']) == 0:
        return render_template('compare.html', phone_details=[])

    phones = Info.query.filter(Info.id.in_(session['compare_list'])).all()
    phone_details = []
    for phone in phones:
        details = Details.query.filter_by(details_id=phone.id).first()
        price = Price.query.filter_by(price_id=phone.id).first()
        brand = Brand.query.filter_by(brand_id=phone.id).first()
        rating = Rating.query.filter_by(ratings_id=phone.id).first()
        phone_details.append({
            'phone': phone,
            'details': details,
            'price': price,
            'brand': brand,
            'rating': rating
        })

    return render_template('compare.html', phone_details=phone_details)

@app.route('/update_compare', methods=['POST'])
def update_compare():
    data = request.json
    phone_id = data.get('phone_id')
    action = data.get('action')

    if not phone_id:
        return jsonify({'error': 'Phone ID is required'}), 400

    # Initialize compare_list in session if not already
    if 'compare_list' not in session:
        session['compare_list'] = []

    # Add or remove the phone_id based on the action
    compare_list = session['compare_list']

    if action == 'add':
        if len(compare_list) < 4 and phone_id not in compare_list:
            compare_list.append(phone_id)
        else:
            return jsonify({'error': 'Comparison list is full or phone already added'}), 400
    elif action == 'remove':
        if phone_id in compare_list:
            compare_list.remove(phone_id)
        else:
            return jsonify({'error': 'Phone not in comparison list'}), 400
    else:
        return jsonify({'error': 'Invalid action'}), 400

    # Update the session compare list
    session['compare_list'] = compare_list
    session.modified = True

    return jsonify({'success': True, 'compare_list': compare_list})

@app.teardown_request
def clear_compare_list(exception=None):
    """Clear compare list after session ends."""
    session.pop('compare_list', None)

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

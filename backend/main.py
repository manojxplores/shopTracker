from docutils.nodes import title
from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from scraper import get_product

app = Flask(__name__)

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///product-details.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Product(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    price: Mapped[str] = mapped_column(String(250), nullable=False)
    product_url : Mapped[str] = mapped_column(String(250), nullable=False)

    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    product_dict = {}
    with app.app_context():
        result = db.session.execute(db.select(Product).order_by(Product.id))
        all_products = result.scalars().all()
    for product in all_products:
        product_dict[product.id] = product.to_dict()
    return jsonify(product_dict)

@app.route('/scrape', methods=['GET', 'POST'])
def scrape():
    if request.method == 'POST':
        product_url = request.form["product_url"]
        try:
            results = get_product(product_url)
            with app.app_context():
                new_product = Product(title=results["title"], price=results["price"], product_url=product_url)
                db.session.add(new_product)
                db.session.commit()
            return jsonify(results)
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    return render_template('index.html')


if __name__ == "__main__":
    app.run()


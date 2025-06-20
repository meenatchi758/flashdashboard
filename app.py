from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dashboard.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# Create tables before first request


# Dashboard route
@app.route("/", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        # Add Product
        if 'product_name' in request.form:
            name = request.form.get("product_name")
            price = float(request.form.get("product_price"))
            new_product = Product(name=name, price=price)
            db.session.add(new_product)
            db.session.commit()
        # Add Sale
        elif 'sale_product' in request.form:
            product = request.form.get("sale_product")
            quantity = int(request.form.get("sale_quantity"))
            total = float(request.form.get("sale_total"))
            new_sale = Sale(product=product, quantity=quantity, total=total)
            db.session.add(new_sale)
            db.session.commit()

        return redirect(url_for("dashboard"))

    products = Product.query.all()
    sales = Sale.query.all()

    total_sales = sum(s.total for s in sales)
    total_products = len(products)

    chart_labels = [s.product for s in sales]
    chart_values = [s.total for s in sales]

    return render_template("dashboard.html", products=products, sales=sales,
                           totals={"total_sales": total_sales, "total_products": total_products},
                           chart_labels=chart_labels, chart_values=chart_values)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # ✅ Create tables manually without @before_first_request
    app.run(debug=True)


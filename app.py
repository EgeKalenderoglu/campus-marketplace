from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Local database for Sprint 1
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///marketplace.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)


@app.route("/")
def index():
    q = request.args.get("q", "")
    listings = Listing.query.order_by(Listing.id.desc())
    if q:
        listings = listings.filter(Listing.title.contains(q))
    return render_template("index.html", listings=listings.all(), q=q)


@app.route("/create", methods=["GET", "POST"])
def create_listing():
    if request.method == "POST":
        title = request.form["title"].strip()
        description = request.form["description"].strip()
        price = request.form["price"].strip()

        if not title or not description or not price:
            return render_template(
                "create_listing.html",
                error="All fields are required."
            )

        try:
            price_value = float(price)

            if price_value < 0:
                raise ValueError

        except ValueError:
            return render_template(
                "create_listing.html",
                error="Please enter a valid price."
            )

        listing = Listing(
            title=title,
            description=description,
            price=price_value
        )

        db.session.add(listing)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("create_listing.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
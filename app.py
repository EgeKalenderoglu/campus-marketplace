from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap5
import os 
import secrets
import extensions
import models
import moderation

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-key-change-me"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///marketplace.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

bootstrap = Bootstrap5(app)

db = extensions.db
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "index"

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(models.User, int(user_id))


@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main"))
    return render_template("index.html")


@app.route("/buy/<int:listing_id>")
def buy_listing(listing_id):
    listing = db.get_or_404(models.Listing, listing_id)
    return render_template("buy_listing.html", listing=listing)


@app.route("/registration", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not email or not username or not password:
            return render_template("index.html", error="All fields are required.")

        if "@" not in email or not email.endswith(".edu"):
            return render_template("index.html", error="Please use a valid university email ending with .edu.")

        if models.User.query.filter((models.User.email == email) | (models.User.username == username)).first():
            return render_template("index.html", error="An account with that email or username already exists.")

        user = models.User(email=email, username=username)
        user.set_password(password)
        user.verification_token = secrets.token_urlsafe(24)
        user.is_verified = False

        db.session.add(user)
        db.session.commit()
        login_user(user)

        return redirect(url_for("verify"))

    return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        remember = bool(request.form.get("remember"))

        user = models.User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user, remember=remember)
            if not user.is_verified:
                return redirect(url_for("verify"))
            return redirect(url_for("main"))

        return render_template("index.html", error="Invalid username or password.")

    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/main")
@login_required
def main():
    q = request.args.get("q", "")
    listings = models.Listing.query.order_by(models.Listing.id.desc())
    if q:
        listings = listings.filter(models.Listing.title.contains(q))
    return render_template("main.html", listings=listings.all(), q=q)


@app.route("/verification", methods=["GET", "POST"])
@login_required
def verify():
    if current_user.is_verified:
        return redirect(url_for("index"))

    if request.method == "POST":
        submitted_code = request.form.get("verification_code", "").strip()
        if submitted_code and submitted_code == current_user.verification_token:
            current_user.is_verified = True
            current_user.verification_token = None
            db.session.commit()
            return redirect(url_for("index"))

        return render_template(
            "verification.html",
            error="That verification code is incorrect. Please try again.",
            verification_code=current_user.verification_token,
            user_email=current_user.email,
        )

    return render_template(
        "verification.html",
        verification_code=current_user.verification_token,
        user_email=current_user.email,
    )


@app.route("/create", methods=["GET", "POST"])
@login_required
def create_listing():
    if not current_user.is_verified:
        return redirect(url_for("verify"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        price = request.form.get("price", "").strip()

        if not title or not description or not price:
            return render_template("create_listing.html", error="All fields are required.")

        try:
            price_value = float(price)
            if price_value < 0:
                raise ValueError
        except ValueError:
            return render_template("create_listing.html", error="Please enter a valid price.")

        moderation_result = moderation.moderate_listing(title, description)

        if not moderation_result["allowed"]:
            return render_template(
                "create_listing.html",
                error=moderation_result["reason"]
            )

        listing = models.Listing(
            title=title,
            description=description,
            price=price_value,
        )

        db.session.add(listing)
        db.session.commit()

        return redirect(url_for("main"))

    return render_template("create_listing.html", name=current_user.username)


@app.route("/user_profile")
@login_required
def user_profile():
    return render_template("user_profile.html", user=current_user)


@app.route("/verificaiton")
def verify_legacy_redirect():
    return redirect(url_for("verify"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    port = int(os.environ.get("PORT", "5002"))
    app.run(debug=True, host="0.0.0.0", port=port)

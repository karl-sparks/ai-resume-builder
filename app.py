"""Main application file"""
import os
from dotenv import load_dotenv
from flask import Flask, redirect, url_for, render_template
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_dance.contrib.google import make_google_blueprint, google

load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey"

login_manager = LoginManager()
login_manager.init_app(app)

blueprint = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    scope=["profile", "email"],
    redirect_url="/google-login",
)
app.register_blueprint(blueprint, url_prefix="/login")


class User(UserMixin):
    pass


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    if resp.ok:
        email = resp.json()["email"]
        user = User()
        user.id = email
        login_user(user)
        return redirect(url_for("home"))
    else:
        return "Error"


@app.route("/google-login")
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    if resp.ok:
        email = resp.json()["email"]
        user = User()
        user.id = email
        login_user(user)
        return redirect(url_for("home"))
    else:
        return "Error"


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/home")
@login_required
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, render_template, jsonify, redirect, url_for
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from secrets import api_key, api_secret
import functools
from db_utils import get_udhaars, insert_into_udhaar, insert_into_users, delete_udhaar, get_user, get_udhaar, \
    get_user_mail_and_name
from mailer import send_mail

app = Flask(
    __name__,
    template_folder='client/templates',
    static_folder='client/static'
)

blueprint = make_twitter_blueprint(
    api_key=api_key,
    api_secret=api_secret,
    redirect_url="/"
)
app.register_blueprint(blueprint, url_prefix="/login")
app.secret_key = "supersekrit"


def login_required(func):
    """Make sure user is logged in before proceeding"""

    @functools.wraps(func)
    def wrapper_login_required(*args, **kwargs):
        if not twitter.authorized:
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)

    return wrapper_login_required


@app.route('/login')
def login():
    if not twitter.authorized:
        return redirect(url_for("twitter.login"))
    else:
        return redirect(url_for("manage"))


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/manage')
@login_required
def manage():
    user_name = twitter.token["screen_name"]
    if len(get_user(user_name)) == 0:
        resp = twitter.get("account/verify_credentials.json",
                           params={'include_email': 'true', "skip_status": 'true', "include_entities": 'false'})
        insert_into_users(user_name, resp.json()["name"], resp.json()["email"])
    udhaars = get_udhaars(user_name)
    return render_template("manage.html", udhaars=udhaars)


@app.route('/add/udhaar', methods=["POST"])
@login_required
def add_udhaar():
    user_name = twitter.token["screen_name"]
    name, email, amount = request.form["name"], request.form["email"], request.form["amount"]
    insert_into_udhaar(user_name, name, email, amount)
    return jsonify(get_udhaars(user_name))


@app.route('/del/udhaar', methods=["POST"])
@login_required
def del_udhaar():
    user_name = twitter.token["screen_name"]
    id = request.form["id"]
    delete_udhaar(id)
    return jsonify(get_udhaars(user_name))


@app.route('/send/mail', methods=["POST"])
@login_required
def send_email():
    user_name = twitter.token["screen_name"]
    id = request.form["id"]
    udhaar = get_udhaar(id)[0]
    user = get_user_mail_and_name(user_name)[0]
    send_mail(udhaar["name"],udhaar["email"],udhaar["amount"],user["email"],user["name"])
    return "Okay"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3500, debug=True)

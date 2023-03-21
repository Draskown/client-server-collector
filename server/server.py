from flask import Flask, request, url_for, \
    jsonify, redirect, render_template, session
from datetime import timedelta
import db_handler as db


EXPIRE_MINUTES = 1

api = Flask(__name__)
api.secret_key = "PpkRXrg9D090ej8RHwQA"
api.permanent_session_lifetime = timedelta(minutes=EXPIRE_MINUTES)


@api.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if request.form["number"]:
            session["cuser"] = request.form["number"]

            if session["cuser"] == "-":
                session["inv_input"] = 0
                return redirect(url_for("invalid_input"))

            if session["cuser"] in db.get_all_users():
                db.set_current_user(session["cuser"], "0")
            else:
                db.set_current_user(session["cuser"], "1")

            return redirect(url_for("current_user"))
    else:
        if "cuser" in session:
            return render_template("index.html", number=session["cuser"])
        else:
            return render_template("index.html", number=None)


@api.route("/currentuser/", methods=["GET", "POST"])
def current_user():
    if request.method == "POST":
        number = request.json["user_number"]
        parameters = request.json["parameters"].values()

        if db.user_exists():
            db.update_parameters(number, parameters)
        else:
            db.insert_user(number, parameters)

        db.write_log(number, "0")

        return "Success", 201

    else:
        info = db.last_message_info()
        if info[0] < EXPIRE_MINUTES:
            session["last_msg_code"] = info[1]
            return redirect(url_for("finale"))
        else:
            if "cuser" in session:
                return render_template("currentuser.html", number=session["cuser"])
            else:
                usr = db.get_current_user()
                return jsonify(usr)


@api.route("/currentuser/handle", methods=["POST", "GET"])
def handle_user():
    if request.method == "POST":
        db.write_log(request.json["user_number"], "1")

        return "Error", 201
    else:
        number = db.get_current_user()["number"]

        return jsonify(db.get_parameters(number))


@api.route("/finale")
def finale():
    if "last_msg_code" in session:
        if session["last_msg_code"] == "1":
            db.set_current_user("-", "-")
            if "cuser" in session:
                session.pop("cuser", None)
            session.pop("last_msg_code", None)
            return render_template("error.html")
        else:
            db.set_current_user("-", "-")
            if "cuser" in session:
                session.pop("cuser", None)
            session.pop("last_msg_code", None)
            return render_template("thanks.html")
    else:
        return redirect(url_for("home"))


@api.route("/invalidinput")
def invalid_input():
    if "inv_input" in session:
        session.pop("inv_input", None)
        session.pop("cuser", None)
        return render_template("invalid_input.html")
    else:
        return redirect(url_for("home"))


if __name__ == "__main__":
    api.run(host='127.0.0.1', port=8888, debug=True)

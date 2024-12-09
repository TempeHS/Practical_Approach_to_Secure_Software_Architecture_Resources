from flask import Flask
from flask import render_template
from flask import request
import db_interface as db_manager

app = Flask(__name__)

is_logged_in = False


@app.route("/", methods=["POST", "GET"])
def index_page():
    global is_logged_in
    if request.method == "POST":
        if request.form["password"].isdigit():
            password = int(request.form["password"])
            email = request.form["email"]
            is_logged_in = db_manager.check_login(email, password)
        app.logger.critical(f"{email} is logged in ? {is_logged_in}")
    return render_template("index.html", is_logged_in=is_logged_in), 200


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/reg", methods=['GET', 'POST'])
def reg():
    print(request.form.get("dolj"))
    if request.method == 'POST':
        if request.form.get("dolj") == "администратор":
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('user'))
    else:
        return render_template("reg.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get("dolj") == "администратор":
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('user'))
    else:
        return render_template("login.html")

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    # if request.method == 'POST':
    #
    # else:
        return render_template("admin.html")

@app.route("/user", methods=['GET', 'POST'])
def user():
    return render_template("user.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
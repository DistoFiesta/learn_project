from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
API_URL = "http://127.0.0.1:8000/products"


@app.route("/")
def index():
    response = requests.get(API_URL)
    products = response.json() if response.status_code == 200 else []
    return render_template("list.html", products=products)


@app.route("/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        old_price_raw = request.form.get("old_price")
        # Если поле пустое, передаем None, иначе конвертируем в float
        old_price_val = float(old_price_raw) if old_price_raw and old_price_raw.strip() else None

        data = {
            "name": request.form["name"],
            "description": request.form["description"],
            "price": float(request.form["price"]),
            "old_price": old_price_val,
            "quantity": int(request.form["quantity"])
        }
        requests.post(API_URL, json=data)
        return redirect(url_for("index"))
    return render_template("form.html", product=None)


@app.route("/edit/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    if request.method == "POST":
        old_price_raw = request.form.get("old_price")
        old_price_val = float(old_price_raw) if old_price_raw and old_price_raw.strip() else None

        data = {
            "name": request.form["name"],
            "description": request.form["description"],
            "price": float(request.form["price"]),
            "old_price": old_price_val,
            "quantity": int(request.form["quantity"])
        }
        requests.put(f"{API_URL}/{product_id}", json=data)
        return redirect(url_for("index"))

    response = requests.get(f"{API_URL}/{product_id}")
    product = response.json() if response.status_code == 200 else None
    return render_template("form.html", product=product)


@app.route("/delete/<int:product_id>")
def delete_product(product_id):
    requests.delete(f"{API_URL}/{product_id}")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(port=5000, debug=True)
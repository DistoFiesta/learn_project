from flask import Flask, render_template, request, redirect, url_for, make_response
import requests

app = Flask(__name__)
API_URL = "http://127.0.0.1:8000/products"


def process_form_data(form):
    base_price = float(form["price"])
    discount_enabled = "has_discount" in form
    discount_pct = form.get("discount_percent")

    if discount_enabled and discount_pct:
        pct = float(discount_pct)
        if pct <= 0 or pct >= 100:
            pct = 0
            old_price = None
            final_price = base_price
        else:
            old_price = base_price
            final_price = base_price * (1 - pct / 100)
    else:
        old_price = None
        final_price = base_price

    urls_raw = form.get("image_urls", "")
    img_list = [url.strip() for url in urls_raw.splitlines() if url.strip()]

    return {
        "name": form["name"],
        # МЯГКИЙ ДОСТУП: Если описания вдруг нет, берем пустую строку, чтобы сервер не падал
        "description": form.get("description", ""),
        "price": round(final_price, 2),
        "old_price": old_price,
        "image_urls": img_list,
        "quantity": int(form["quantity"])
    }


@app.route("/")
def index():
    r = requests.get(API_URL)
    return render_template("list.html", products=r.json() if r.status_code == 200 else [])


@app.route("/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        data = process_form_data(request.form)
        requests.post(API_URL, json=data)
        return redirect(url_for("index"))
    return render_template("form.html", product=None)


@app.route("/edit/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    if request.method == "POST":
        data = process_form_data(request.form)
        requests.put(f"{API_URL}/{product_id}", json=data)
        return redirect(url_for("index"))
    r = requests.get(f"{API_URL}/{product_id}")
    return render_template("form.html", product=r.json())


@app.route("/delete-single/<int:product_id>")
def delete_single(product_id):
    requests.delete(f"{API_URL}/{product_id}")
    return redirect(url_for("index"))


@app.route("/delete-bulk", methods=["POST"])
def delete_bulk():
    ids = request.form.getlist("selected_ids")
    if ids:
        requests.post(f"{API_URL}/bulk-delete", json=[int(i) for i in ids])
    return redirect(url_for("index"))


@app.route("/toggle-theme")
def toggle_theme():
    res = make_response(redirect(request.referrer or "/"))
    theme = "dark" if request.cookies.get("theme") == "light" else "light"
    res.set_cookie("theme", theme)
    return res


if __name__ == "__main__":
    app.run(port=5000, debug=True)
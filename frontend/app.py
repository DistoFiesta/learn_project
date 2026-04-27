from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# Ссылка на твой бэкенд FastAPI
API_URL = "http://127.0.0.1:8000/products"


@app.route("/")
def index():
    """Главная страница: запрашиваем список товаров с бэкенда и рендерим HTML."""
    response = requests.get(API_URL)
    products = response.json() if response.status_code == 200 else []
    return render_template("list.html", products=products)


@app.route("/add", methods=["GET", "POST"])
def add_product():
    """Страница добавления товара."""
    if request.method == "POST":
        old_price_val = request.form.get("old_price")
        data = {
            "name": request.form["name"],
            "description": request.form["description"],
            "price": float(request.form["price"]),
            "old_price": float(old_price_val) if old_price_val else None,  # Забираем старую цену
            "quantity": int(request.form["quantity"])
        }
        # Отправляем POST-запрос на бэкенд (как ты делал в Swagger)
        requests.post(API_URL, json=data)
        return redirect(url_for("index"))

    # Если метод GET, просто показываем пустую форму
    return render_template("form.html", product=None)


@app.route("/edit/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    """Страница редактирования товара."""
    if request.method == "POST":
        old_price_val = request.form.get("old_price")
        data = {
            "name": request.form["name"],
            "description": request.form["description"],
            "price": float(request.form["price"]),
            "old_price": float(old_price_val) if old_price_val else None,  # Забираем старую цену
            "quantity": int(request.form["quantity"])
        }
        # Отправляем PUT-запрос на бэкенд для обновления
        requests.put(f"{API_URL}/{product_id}", json=data)
        return redirect(url_for("index"))

    # Если метод GET, запрашиваем текущие данные товара, чтобы подставить их в форму
    response = requests.get(f"{API_URL}/{product_id}")
    product = response.json() if response.status_code == 200 else None
    return render_template("form.html", product=product)


@app.route("/delete/<int:product_id>")
def delete_product(product_id):
    """Удаление товара (вызывается по кнопке)."""
    requests.delete(f"{API_URL}/{product_id}")
    return redirect(url_for("index"))


if __name__ == "__main__":
    # Запускаем Flask на порту 5000 (чтобы не конфликтовать с FastAPI на 8000)
    app.run(port=5000, debug=True)
from flask import Flask, render_template

app = Flask(__name__)

# Пример данных (вместо этого используйте свою логику получения данных из базы данных)
categories = {
    'clothing': {'name': 'Одежда', 'products': [{'id': 1, 'name': 'Футболка', 'price': 20, 'description': 'Хорошая футболка'}, {'id': 2, 'name': 'Джинсы', 'price': 50, 'description': 'Отличные джинсы'}]},
    'shoes': {'name': 'Обувь', 'products': [{'id': 3, 'name': 'Кроссовки', 'price': 70, 'description': 'Удобные кроссовки'}, {'id': 4, 'name': 'Ботинки', 'price': 100, 'description': 'Красивые ботинки'}]},
}

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/clothing')
def clothing():
    return render_template('clothing.html', category=categories['clothing']['name'], products=categories['clothing']['products'])

@app.route('/shoes')
def shoes():
    return render_template('shoes.html', category=categories['shoes']['name'], products=categories['shoes']['products'])

@app.route('/product/<int:product_id>')
def product(product_id):
    # Предполагается, что product_id - это уникальный идентификатор товара
    # Для примера, возвращаем просто словарь с данными о товаре
    product_data = {'id': product_id, 'name': 'Пример товара', 'price': 50, 'description': 'Описание товара'}
    return render_template('product.html', product=product_data)

if __name__ == '__main__':
    app.run(debug=True)

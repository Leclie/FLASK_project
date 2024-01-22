from flask_bcrypt import Bcrypt
from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # SQLite база данных
app.config['SECRET_KEY'] = 'your_secret_key'  # Замените на свой секретный ключ
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

# Модель для пользователя в базе данных
class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

# Форма для регистрации
class RegistrationForm(FlaskForm):
    first_name = StringField('Имя', validators=[validators.DataRequired()])
    last_name = StringField('Фамилия', validators=[validators.DataRequired()])
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('Пароль', validators=[validators.DataRequired(), validators.Length(min=6)])
    confirm_password = PasswordField('Подтвердить пароль', validators=[validators.DataRequired(), validators.EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')


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




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        # Создание cookie
        response = make_response(redirect(url_for('welcome')))
        response.set_cookie('user_data', f'{name},{email}')

        return response

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Проверка совпадения паролей
        if form.password.data != form.confirm_password.data:
            flash('Пароли не совпадают', 'error')  # Отправляем сообщение об ошибке в механизм flash
            return redirect(url_for('register'))  # Перенаправляем обратно на страницу регистрации


        # Шифрование пароля (вы можете использовать более безопасные методы)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # Создание нового пользователя
        new_user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Возвращение на главную страницу после успешной регистрации (вы можете изменить на другой редирект)
        return redirect(url_for('home'))

    return render_template('register.html', form=form)

@app.route('/welcome')
def welcome():
    user_cookie = request.cookies.get('user_data')
    if user_cookie:
        name, _ = user_cookie.split(',')
        return render_template('welcome.html', name=name)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    # Удаление cookie
    response = make_response(redirect(url_for('login')))
    response.delete_cookie('user_data')
    return response



if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создание таблиц в базе данных
    app.run(debug=True)
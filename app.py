from flask import Flask, redirect, url_for, flash, session, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
import traceback

app = Flask(__name__)

# Убедимся, что директория instance существует
instance_path = os.path.join(os.getcwd(), 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)
    print(f"Создана директория для базы данных: {instance_path}")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# Use environment variable for secret key or set a random value
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24).hex())
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Account(db.Model):  
    __tablename__ = 'account' 

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), nullable=False, unique=True)  
    password = db.Column(db.String(128), nullable=False)
    pochta = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, login, password, pochta):  
        self.login = login
        self.password = generate_password_hash(password)  
        self.pochta = pochta

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Database(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    opis = db.Column(db.String(1000), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    teg1 = db.Column(db.String(50), nullable=False)
    teg2 = db.Column(db.String(50), nullable=True)
    teg3 = db.Column(db.String(50), nullable=True)
    image = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, nullable=True)

    def __init__(self, opis, name, teg1, teg2=None, teg3=None, image=None, user_id=None):
        self.opis = opis
        self.name = name
        self.teg1 = teg1
        self.teg2 = teg2
        self.teg3 = teg3
        self.image = image
        self.user_id = user_id


@app.route('/', methods=['GET', 'POST'])
def glavna():
    if request.method == 'POST':
        try:
            login = request.form.get('login')
            password = request.form.get('password')
            pochta = request.form.get('pochta')

            print(f"Получены данные: login={login}, password={len(password) * '*'}, pochta={pochta}")
            
            if not login or not password or not pochta:
                flash("Все поля должны быть заполнены", 'error')
                return render_template('glavna.html', js_file=url_for('static', filename='главная.js'), css_file=url_for('static', filename='главня.css'))
            
            # Проверяем, есть ли уже такой логин или email
            existing_login = Account.query.filter(Account.login == login).first()
            existing_email = Account.query.filter(Account.pochta == pochta).first()
            
            if existing_login and existing_email:
                flash("Пользователь с таким логином и email уже существует", 'error')
                return render_template('glavna.html', js_file=url_for('static', filename='главная.js'), css_file=url_for('static', filename='главня.css'))
            elif existing_login:
                flash("Пользователь с таким логином уже существует", 'error')
                return render_template('glavna.html', js_file=url_for('static', filename='главная.js'), css_file=url_for('static', filename='главня.css'))
            elif existing_email:
                flash("Пользователь с таким email уже существует", 'error')
                return render_template('glavna.html', js_file=url_for('static', filename='главная.js'), css_file=url_for('static', filename='главня.css'))

            # Создаем новый аккаунт
            new_account = Account(login=login, password=password, pochta=pochta)
            db.session.add(new_account)
            db.session.commit()
            print(f"Новый аккаунт создан: ID={new_account.id}")

            flash('Account created successfully!', 'success')
            return render_template('glavna.html', js_file=url_for('static', filename='главная.js'), css_file=url_for('static', filename='главня.css'))
        except Exception as e:
            db.session.rollback()
            print(f"Ошибка при создании аккаунта: {str(e)}")
            print(traceback.format_exc())
            flash(f"Error: {str(e)}", 'error')
            return render_template('glavna.html', js_file=url_for('static', filename='главная.js'), css_file=url_for('static', filename='главня.css'))

    # Process GET request (display items and filter)
    selected_genres = request.args.getlist('genre')

    # Получаем все записи из базы данных
    try:
        items = Database.query.all()
        print(f"Загружено {len(items)} записей из базы данных")
    except Exception as e:
        print(f"Ошибка при загрузке данных: {str(e)}")
        items = []

    if selected_genres:
        filtered_items = []
        for item in items:
            item_tags = [item.teg1, item.teg2, item.teg3]
            for genre in selected_genres:
                if any(genre.lower() in str(tag).lower() for tag in item_tags if tag):
                    filtered_items.append(item)
                    break
        items = filtered_items

    return render_template('glavna.html', glavna=items, js_file=url_for('static', filename='главная.js'), css_file=url_for('static', filename='главня.css'))


@app.route('/karta1/<int:id>')
def karta1(id):
    karta1_item = Database.query.get_or_404(id)
    if karta1_item:
        items = [karta1_item]
        return render_template('karta1.html', items=items, css_file=url_for('static', filename='karta1.css'))
    else:
        flash('Item not found')
        return redirect(url_for('glavna'))


@app.route('/Profile/<int:user_id>')
def prof(user_id):
    profile_item = Database.query.get(user_id)

    if profile_item:
        items = [profile_item]
        return render_template('Profile.html', items=items, css_file=url_for('static', filename='Profile.css'))
    else:
        flash('Profile not found')
        return redirect(url_for('glavna'))

@app.route('/check_availability', methods=['POST'])
def check_availability():
    """API для проверки доступности логина или email"""
    data = request.get_json()
    field_type = data.get('type')
    value = data.get('value')
    
    if not field_type or not value:
        return jsonify({'error': 'Неверные параметры запроса'}), 400
    
    if field_type == 'login':
        existing = Account.query.filter(Account.login == value).first()
    elif field_type == 'email':
        existing = Account.query.filter(Account.pochta == value).first()
    else:
        return jsonify({'error': 'Неверный тип поля'}), 400
    
    return jsonify({'available': existing is None})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("База данных создана/обновлена")
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 
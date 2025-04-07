from flask import Flask, redirect, url_for, flash, session, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
import traceback
from werkzeug.utils import secure_filename
import time
from sqlalchemy import or_
from models import Account, Database, db

app = Flask(__name__)

# Убедимся, что директория instance существует
instance_path = os.path.join(os.getcwd(), 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)
    print(f"Создана директория для базы данных: {instance_path}")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# Use environment variable for secret key or set a random value
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24).hex())
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Настройка для загрузки файлов
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Инициализация базы данных
db.init_app(app)

# Создание таблиц
with app.app_context():
    db.create_all()
    print("Таблицы базы данных созданы")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
                return render_template('glavna.html', 
                                    js_file=url_for('static', filename='главная.js'), 
                                    css_file=url_for('static', filename='главня.css'),
                                    user_logged_in='user_id' in session)
            
            # Проверяем, есть ли уже такой логин или email
            existing_login = Account.query.filter(Account.login == login).first()
            existing_email = Account.query.filter(Account.pochta == pochta).first()
            
            if existing_login and existing_email:
                flash("Пользователь с таким логином и email уже существует", 'error')
                return render_template('glavna.html', 
                                    js_file=url_for('static', filename='главная.js'), 
                                    css_file=url_for('static', filename='главня.css'),
                                    user_logged_in='user_id' in session)
            elif existing_login:
                flash("Пользователь с таким логином уже существует", 'error')
                return render_template('glavna.html', 
                                    js_file=url_for('static', filename='главная.js'), 
                                    css_file=url_for('static', filename='главня.css'),
                                    user_logged_in='user_id' in session)
            elif existing_email:
                flash("Пользователь с таким email уже существует", 'error')
                return render_template('glavna.html', 
                                    js_file=url_for('static', filename='главная.js'), 
                                    css_file=url_for('static', filename='главня.css'),
                                    user_logged_in='user_id' in session)

            new_account = Account(login=login, password=password, pochta=pochta)
            db.session.add(new_account)
            db.session.commit()
            print(f"Новый аккаунт создан: ID={new_account.id}")

            session['user_id'] = new_account.id
            session['user_login'] = new_account.login
            session['user_logged_in'] = True

            flash('Аккаунт успешно создан! Вы автоматически вошли в систему.', 'success')
            return redirect(url_for('glavna'))
        except Exception as e:
            db.session.rollback()
            print(f"Ошибка при создании аккаунта: {str(e)}")
            print(traceback.format_exc())
            flash(f"Ошибка: {str(e)}", 'error')
            return render_template('glavna.html', 
                                js_file=url_for('static', filename='главная.js'), 
                                css_file=url_for('static', filename='главня.css'),
                                user_logged_in='user_id' in session)

    # Process GET request (display items and filter)
    selected_genres = request.args.getlist('genre')

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

    return render_template('glavna.html', 
                         glavna=items, 
                         js_file=url_for('static', filename='главная.js'), 
                         css_file=url_for('static', filename='главня.css'),
                         user_logged_in='user_id' in session)


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

@app.route('/add_game', methods=['POST'])
def add_game():
    try:
        name = request.form.get('name')
        opis = request.form.get('opis')
        teg1 = request.form.get('teg1')
        teg2 = request.form.get('teg2')
        teg3 = request.form.get('teg3')
        
        # Обработка загруженного файла
        if 'image' in request.files:
            file = request.files['image']
            if file.filename:
                filename = secure_filename(file.filename)
                file_path = os.path.join('uploads', filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                file_path = None
        else:
            file_path = None

        # Создаем новую игру
        new_game = Database(
            name=name,
            opis=opis,
            teg1=teg1,
            teg2=teg2,
            teg3=teg3,
            image=file_path,
            user_id=session.get('user_id'),
            login=session.get('user_login')
        )

        db.session.add(new_game)
        db.session.commit()

        flash('Игра успешно добавлена!')
        return redirect(url_for('index'))

    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при добавлении игры: {str(e)}')
        return redirect(url_for('index'))

@app.route('/search')
def search():
    query = request.args.get('query', '').lower()
    if not query:
        return redirect('/')

    # Если вы используете SQLAlchemy:
    search_results = Database.query.filter(
        or_(
            Database.name.ilike(f'%{query}%'),
            Database.opis.ilike(f'%{query}%'),
            Database.teg1.ilike(f'%{query}%'),
            Database.teg2.ilike(f'%{query}%'),
            Database.teg3.ilike(f'%{query}%')
        )
    ).all()
    
    return render_template('glavna.html', 
                         glavna=search_results,
                         css_file=url_for('static', filename='styles.css'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        email = request.form.get('pochta')

        print(f"Попытка регистрации: login={login}, email={email}")  # Логирование для отладки

        # Проверяем, существует ли пользователь
        if Account.query.filter_by(login=login).first():
            flash('Пользователь с таким логином уже существует', 'error')
            return redirect(url_for('glavna'))

        if Account.query.filter_by(pochta=email).first():
            flash('Пользователь с таким email уже существует', 'error')
            return redirect(url_for('glavna'))

        try:
            # Создаем нового пользователя
            new_user = Account(
                login=login,
                password=password,  # Пароль будет хеширован в конструкторе Account
                pochta=email
            )
            db.session.add(new_user)
            db.session.commit()
            
            print(f"Новый пользователь создан: {new_user.login}")  # Логирование для отладки
            
            # Автоматически входим в аккаунт после регистрации
            session['user_id'] = new_user.id
            session['user_login'] = new_user.login
            session['user_logged_in'] = True
            
            flash('Регистрация успешна! Вы автоматически вошли в систему.', 'success')
            return redirect(url_for('glavna'))
            
        except Exception as e:
            print(f"Ошибка при регистрации: {str(e)}")  # Логирование для отладки
            db.session.rollback()
            flash('Произошла ошибка при регистрации', 'error')
            return redirect(url_for('glavna'))
    
    return redirect(url_for('glavna'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        
        print(f"Попытка входа: login={login}")  # Логирование для отладки
        
        user = Account.query.filter_by(login=login).first()
        
        if user:
            print(f"Пользователь найден: {user.login}")  # Логирование для отладки
            print(f"Хеш пароля в БД: {user.password}")  # Логирование для отладки
            if user.check_password(password):
                print("Пароль верный")  # Логирование для отладки
                session['user_id'] = user.id
                session['user_login'] = user.login
                session['user_logged_in'] = True
                flash('Вы успешно вошли в систему!', 'success')
                return redirect(url_for('glavna'))
            else:
                print("Неверный пароль")  # Логирование для отладки
                print(f"Введенный пароль: {password}")  # Логирование для отладки
                flash('Неверный пароль', 'error')
        else:
            print("Пользователь не найден")  # Логирование для отладки
            flash('Пользователь с таким логином не найден', 'error')
        
        return redirect(url_for('glavna'))
    
    return redirect(url_for('glavna'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/profile/<int:user_id>')
def profile(user_id):
    if 'user_id' not in session:
        flash('Пожалуйста, войдите в систему')
        return redirect(url_for('index'))
    
    user = Account.query.get_or_404(user_id)
    return render_template('profile.html', user=user, user_logged_in=True)

@app.route('/settings')
def settings():
    if 'user_id' not in session:
        return redirect(url_for('glavna'))
    
    user = Account.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect(url_for('glavna'))
    
    return render_template('settings.html', user=user)

@app.route('/')
def index():
    user_logged_in = 'user_id' in session
    return render_template('glavna.html', user_logged_in=user_logged_in)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 
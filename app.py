from flask import Flask, redirect, url_for, flash, session, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
import traceback
from werkzeug.utils import secure_filename
import time
from sqlalchemy import or_

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

# Настройка для загрузки файлов
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    login = db.Column(db.String(20), nullable=False, default='admin')
    password = db.Column(db.String(128), nullable=False, default='admin')

    def __init__(self, opis, name, teg1, teg2=None, teg3=None, image=None, user_id=None, login='admin', password='admin'):
        self.opis = opis
        self.name = name
        self.teg1 = teg1
        self.teg2 = teg2
        self.teg3 = teg3
        self.image = image
        self.user_id = user_id
        self.login = login
        self.password = generate_password_hash(password)

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

@app.route('/add_game', methods=['POST'])
def add_game():
    try:
        # Получаем данные из формы
        name = request.form.get('name')
        opis = request.form.get('opis')
        teg1 = request.form.get('teg1')
        teg2 = request.form.get('teg2')
        teg3 = request.form.get('teg3')
        
        # Проверяем наличие файла
        if 'image' not in request.files:
            flash('Изображение не выбрано', 'error')
            return redirect(url_for('glavna'))
            
        file = request.files['image']
        if file.filename == '':
            flash('Изображение не выбрано', 'error')
            return redirect(url_for('glavna'))
            
        if file and allowed_file(file.filename):
            # Сохраняем файл
            filename = secure_filename(file.filename)
            # Создаем уникальное имя файла
            unique_filename = f"{int(time.time())}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            
            # Создаем запись в базе данных
            new_game = Database(
                name=name,
                opis=opis,
                teg1=teg1,
                teg2=teg2 if teg2 else None,
                teg3=teg3 if teg3 else None,
                image=f"uploads/{unique_filename}",
                login='admin',
                password='admin'
            )
            
            db.session.add(new_game)
            db.session.commit()
            
            flash('Игра успешно добавлена!', 'success')
        else:
            flash('Неподдерживаемый формат файла', 'error')
            
    except Exception as e:
        db.session.rollback()
        flash(f'Произошла ошибка при добавлении игры: {str(e)}', 'error')
        
    return redirect(url_for('glavna'))

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

    # Если вы используете список/словарь:
    # search_results = []
    # for game in glavna:
    #     if (query in game['name'].lower() or 
    #         query in game['opis'].lower() or 
    #         query in game['teg1'].lower() or 
    #         (game['teg2'] and query in game['teg2'].lower()) or 
    #         (game['teg3'] and query in game['teg3'].lower())):
    #         search_results.append(game)

    return render_template('glavna.html', 
                         glavna=search_results,
                         css_file=url_for('static', filename='styles.css'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        email = request.form.get('pochta')

        # Проверяем, существует ли пользователь
        if Account.query.filter_by(login=login).first():
            flash('Пользователь с таким логином уже существует', 'error')
            return redirect(url_for('glavna'))

        if Account.query.filter_by(pochta=email).first():
            flash('Пользователь с таким email уже существует', 'error')
            return redirect(url_for('glavna'))

        try:
            # Создаем нового пользователя
            hashed_password = generate_password_hash(password)
            new_user = Account(
                login=login,
                password=hashed_password,
                pochta=email
            )
            db.session.add(new_user)
            db.session.commit()
            
            # Автоматически входим в аккаунт после регистрации
            session['user_id'] = new_user.id
            flash('Регистрация успешна!', 'success')
            return redirect(url_for('glavna'))
            
        except Exception as e:
            print(e)  # для отладки
            db.session.rollback()
            flash('Произошла ошибка при регистрации', 'error')
            return redirect(url_for('glavna'))
    
    # Если GET запрос, перенаправляем на главную
    return redirect(url_for('glavna'))

@app.route('/login', methods=['POST'])
def login():
    login = request.form.get('login')
    password = request.form.get('password')
    
    user = Account.query.filter_by(login=login).first()
    
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        session['user_logged_in'] = True
        return redirect(url_for('profile', user_id=user.id))
    else:
        flash('Неверный логин или пароль')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Вы вышли из аккаунта', 'success')
    return redirect(url_for('glavna'))

@app.route('/profile/<int:user_id>')
def profile(user_id):
    # Получаем пользователя из базы данных
    user = Account.query.get_or_404(user_id)
    
    # Проверяем, авторизован ли текущий пользователь
    if 'user_id' not in session:
        flash('Пожалуйста, войдите в систему')
        return redirect(url_for('index'))
    
    # Получаем дополнительные данные пользователя (если есть)
    user_data = {
        'username': user.login,
        'email': user.pochta,
        # Добавьте другие поля, которые хотите отображать
    }
    
    return render_template('profile.html', user=user_data)

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
    # Проверяем, авторизован ли пользователь
    user_logged_in = 'user_id' in session
    return render_template('glavna.html', user_logged_in=user_logged_in)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("База данных создана/обновлена")
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 
# Техническая документация проекта "Каталог игр"

## 1. Введение

### 1.1. Цель документа
Данный документ содержит подробное описание всех используемых технологий, тегов и компонентов в проекте "Каталог игр". Документация предназначена для разработчиков, которые будут работать с проектом.

### 1.2. Структура документа
Документ разделен на следующие основные разделы:
- Backend технологии
- Frontend технологии
- База данных
- Безопасность
- Развертывание

## 2. Backend технологии

### 2.1. Flask Framework
```python
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
```

#### 2.1.1. Основные компоненты Flask и их работа
1. **Flask** - основной класс приложения
   - Создает WSGI-приложение
   - Управляет маршрутизацией запросов
   - Обрабатывает HTTP-запросы и ответы
   - Пример работы:
   ```python
   app = Flask(__name__)
   @app.route('/')
   def index():
       return 'Hello World'
   ```

2. **render_template** - рендеринг HTML шаблонов
   - Принимает имя шаблона и контекстные переменные
   - Использует Jinja2 для шаблонизации
   - Пример работы:
   ```python
   @app.route('/profile')
   def profile():
       return render_template('profile.html', user=current_user)
   ```

3. **request** - обработка HTTP запросов
   - Получает данные из форм
   - Обрабатывает GET и POST параметры
   - Пример работы:
   ```python
   @app.route('/login', methods=['POST'])
   def login():
       username = request.form['username']
       password = request.form['password']
   ```

4. **redirect** - перенаправление
   - Создает HTTP-ответ с кодом 302
   - Перенаправляет пользователя на другой URL
   - Пример работы:
   ```python
   @app.route('/logout')
   def logout():
       logout_user()
       return redirect(url_for('index'))
   ```

5. **url_for** - генерация URL
   - Создает URL для указанного маршрута
   - Учитывает параметры маршрута
   - Пример работы:
   ```python
   url_for('profile', user_id=1)  # -> /profile/1
   ```

6. **flash** - система сообщений
   - Сохраняет сообщения в сессии
   - Отображает их при следующем запросе
   - Пример работы:
   ```python
   flash('Сообщение успешно отправлено')
   ```

### 2.2. SQLAlchemy ORM
```python
db = SQLAlchemy()
```

#### 2.2.1. Модели данных и их работа
1. **Account** - модель пользователя
   ```python
   class Account(UserMixin, db.Model):
       id = db.Column(db.Integer, primary_key=True)
       login = db.Column(db.String(100), unique=True)
       pochta = db.Column(db.String(100), unique=True)
       password = db.Column(db.String(100))
   ```
   - Работа с пользователями:
   ```python
   # Создание пользователя
   user = Account(login='user', pochta='user@example.com')
   user.password = generate_password_hash('password')
   db.session.add(user)
   db.session.commit()

   # Поиск пользователя
   user = Account.query.filter_by(login='user').first()
   ```

2. **Database** - модель игр
   ```python
   class Database(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       name = db.Column(db.String(100))
       description = db.Column(db.Text)
       image = db.Column(db.String(255))
       genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
   ```
   - Работа с играми:
   ```python
   # Добавление игры
   game = Database(name='Game', description='Description')
   db.session.add(game)
   db.session.commit()

   # Получение всех игр
   games = Database.query.all()
   ```

3. **Genre** - модель жанров
   ```python
   class Genre(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       name = db.Column(db.String(50))
   ```
   - Работа с жанрами:
   ```python
   # Создание жанра
   genre = Genre(name='Action')
   db.session.add(genre)
   db.session.commit()
   ```

### 2.3. Flask-Login
```python
login_manager = LoginManager()
login_manager.login_view = 'login'
```

#### 2.3.1. Работа с аутентификацией
1. **Инициализация**
   ```python
   login_manager.init_app(app)
   @login_manager.user_loader
   def load_user(user_id):
       return Account.query.get(int(user_id))
   ```

2. **Вход пользователя**
   ```python
   @app.route('/login', methods=['POST'])
   def login():
       user = Account.query.filter_by(login=request.form['login']).first()
       if user and check_password_hash(user.password, request.form['password']):
           login_user(user)
           return redirect(url_for('index'))
   ```

3. **Защита маршрутов**
   ```python
   @app.route('/profile')
   @login_required
   def profile():
       return render_template('profile.html')
   ```

## 3. Frontend технологии

### 3.1. HTML5

#### 3.1.1. Основные теги и их работа
```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{% endblock %}</title>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
```

1. **Структурные теги**
   - `<header>` - шапка сайта
     ```html
     <header>
         <nav>Навигация</nav>
         <div class="user-info">Информация о пользователе</div>
     </header>
     ```
   
   - `<nav>` - навигационное меню
     ```html
     <nav>
         <a href="/">Главная</a>
         <a href="/games">Игры</a>
         <a href="/profile">Профиль</a>
     </nav>
     ```
   
   - `<main>` - основное содержимое
     ```html
     <main>
         <h1>Заголовок</h1>
         <p>Основной контент</p>
     </main>
     ```

2. **Формы и их работа**
   ```html
   <form method="POST" enctype="multipart/form-data">
       <input type="text" name="name" required>
       <input type="email" name="email" required>
       <input type="password" name="password" required>
       <input type="file" name="image" accept="image/*">
       <button type="submit">Отправить</button>
   </form>
   ```
   - `method="POST"` - отправка данных на сервер
   - `enctype="multipart/form-data"` - для загрузки файлов
   - `required` - обязательные поля
   - `accept="image/*"` - только изображения

### 3.2. CSS3

#### 3.2.1. Стили и их работа
1. **Основные селекторы**
   ```css
   .class-name {
       color: #333;
       font-size: 16px;
   }
   ```
   - Применяет стили к элементам с классом `class-name`

2. **Flexbox**
   ```css
   .container {
       display: flex;
       flex-direction: row;
       justify-content: center;
       align-items: center;
   }
   ```
   - `display: flex` - включает flex-контейнер
   - `flex-direction: row` - горизонтальное расположение
   - `justify-content: center` - центрирование по горизонтали
   - `align-items: center` - центрирование по вертикали

3. **Grid**
   ```css
   .grid-container {
       display: grid;
       grid-template-columns: repeat(3, 1fr);
       gap: 20px;
   }
   ```
   - Создает сетку из 3 колонок
   - Равномерное распределение пространства
   - Отступы между элементами 20px

4. **Медиа-запросы**
   ```css
   @media (max-width: 768px) {
       .container {
           flex-direction: column;
       }
   }
   ```
   - Адаптивный дизайн для мобильных устройств
   - Изменение layout при ширине экрана < 768px

### 3.3. JavaScript

#### 3.3.1. Обработка событий и их работа
1. **Инициализация**
   ```javascript
   document.addEventListener('DOMContentLoaded', function() {
       // Код выполняется после загрузки DOM
       initForms();
       initModals();
   });
   ```

2. **Обработка кликов**
   ```javascript
   element.addEventListener('click', function(e) {
       e.preventDefault();
       // Предотвращает стандартное поведение
       // Выполняет кастомные действия
   });
   ```

3. **AJAX запросы**
   ```javascript
   fetch('/api/endpoint', {
       method: 'POST',
       headers: {
           'Content-Type': 'application/json'
       },
       body: JSON.stringify(data)
   })
   .then(response => response.json())
   .then(data => {
       // Обработка ответа
   });
   ```
   - Асинхронные запросы к серверу
   - Обработка ответов в формате JSON
   - Обновление UI без перезагрузки страницы

## 4. База данных

### 4.1. SQLite
- Легковесная реляционная БД
- Хранение в файле
- Поддержка транзакций
- Встроенная в Python

#### 4.1.1. Работа с SQLite
1. **Подключение**
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
   db.init_app(app)
   ```

2. **Создание таблиц**
   ```python
   with app.app_context():
       db.create_all()
   ```

3. **Работа с данными**
   ```python
   # Добавление записи
   new_record = Model(data='value')
   db.session.add(new_record)
   db.session.commit()

   # Получение записей
   records = Model.query.all()
   ```

### 4.2. Таблицы и их работа

#### 4.2.1. Account
```sql
CREATE TABLE account (
    id INTEGER PRIMARY KEY,
    login VARCHAR(100) UNIQUE,
    pochta VARCHAR(100) UNIQUE,
    password VARCHAR(100)
);
```
- Хранение данных пользователей
- Уникальные логин и email
- Хешированные пароли

#### 4.2.2. Database (игры)
```sql
CREATE TABLE database (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
    image VARCHAR(255),
    genre_id INTEGER,
    FOREIGN KEY (genre_id) REFERENCES genre(id)
);
```
- Хранение информации об играх
- Связь с таблицей жанров
- Пути к изображениям

#### 4.2.3. Genre
```sql
CREATE TABLE genre (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50)
);
```
- Хранение жанров игр
- Связь с таблицей игр

## 5. Безопасность

### 5.1. Аутентификация
- Хеширование паролей (Werkzeug)
- Сессии (Flask-Login)
- CSRF защита

#### 5.1.1. Работа с безопасностью
1. **Хеширование паролей**
   ```python
   # Создание хеша
   password_hash = generate_password_hash('password')
   
   # Проверка пароля
   check_password_hash(password_hash, 'password')
   ```

2. **Сессии**
   ```python
   # Сохранение в сессии
   session['user_id'] = user.id
   
   # Получение из сессии
   user_id = session.get('user_id')
   ```

3. **CSRF защита**
   ```python
   from flask_wtf.csrf import CSRFProtect
   csrf = CSRFProtect(app)
   ```

### 5.2. Валидация данных
```python
if not all([name, description, genre_id]):
    flash('Все поля обязательны для заполнения')
    return redirect(url_for('add_game'))
```
- Проверка обязательных полей
- Валидация типов данных
- Обработка ошибок

### 5.3. Загрузка файлов
```python
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
```
- Проверка расширений файлов
- Генерация уникальных имен
- Безопасное хранение

## 6. Развертывание

### 6.1. Требования
- Python 3.8+
- pip
- virtualenv (рекомендуется)

### 6.2. Установка и работа
```bash
# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Установка зависимостей
pip install -r requirements.txt

# Инициализация БД
flask db init
flask db migrate
flask db upgrade
```

### 6.3. Запуск
```bash
flask run
```
- Запуск development сервера
- Автоматическая перезагрузка при изменениях
- Отладка ошибок

## 7. Оптимизация

### 7.1. Производительность
- Кэширование запросов
- Оптимизация изображений
- Минификация CSS/JS

#### 7.1.1. Работа с оптимизацией
1. **Кэширование**
   ```python
   from flask_caching import Cache
   cache = Cache(app)
   
   @app.route('/')
   @cache.cached(timeout=300)
   def index():
       return render_template('index.html')
   ```

2. **Оптимизация изображений**
   ```python
   from PIL import Image
   
   def optimize_image(image_path):
       img = Image.open(image_path)
       img.thumbnail((800, 800))
       img.save(image_path, optimize=True, quality=85)
   ```

### 7.2. Безопасность
- HTTPS
- Защита от SQL-инъекций
- Валидация входных данных

## 8. Мониторинг и логирование

### 8.1. Логирование
```python
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
```
- Запись событий в файл
- Разные уровни логирования
- Форматирование сообщений

### 8.2. Обработка ошибок
```python
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
```
- Пользовательские страницы ошибок
- Откат транзакций при ошибках
- Логирование ошибок

## 9. Тестирование

### 9.1. Unit тесты
```python
import unittest
from app import app, db

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
```
- Тестирование отдельных компонентов
- Изолированное тестирование
- Автоматизация тестов

### 9.2. Интеграционные тесты
- Тестирование API
- Тестирование форм
- Тестирование БД

## 10. Документация API

### 10.1. Endpoints
- GET / - главная страница
- GET /login - форма входа
- POST /login - аутентификация
- GET /register - форма регистрации
- POST /register - создание аккаунта
- GET /profile/<id> - профиль пользователя
- GET /game/<id> - страница игры
- POST /add_game - добавление игры

## 11. Рекомендации по разработке

### 11.1. Code Style
- PEP 8 для Python
- ESLint для JavaScript
- Prettier для форматирования

### 11.2. Git Workflow
- Feature branches
- Pull requests
- Code review

## 12. Поддержка и обслуживание

### 12.1. Резервное копирование
- Регулярное копирование БД
- Хранение медиафайлов
- Версионирование кода

### 12.2. Обновления
- Обновление зависимостей
- Миграции БД
- Тестирование изменений

## 13. Заключение

### 13.1. Итоги
Проект использует современный стек технологий:
- Flask для backend
- SQLAlchemy для работы с БД
- Современный фронтенд (HTML5, CSS3, JavaScript)
- Системы безопасности и валидации

### 13.2. Перспективы развития
- Масштабирование
- Добавление новых функций
- Улучшение производительности
- Расширение документации 
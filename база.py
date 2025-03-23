from flask import Flask, redirect, url_for, flash, session, request, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key'

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
        login = request.form.get('login')
        password = request.form.get('password')
        pochta = request.form.get('pochta')

        existing_account = Account.query.filter((Account.login == login) | (Account.pochta == pochta)).first()
        if existing_account:
            flash("Username or Email Already Exists", 'error')
            return render_template('glavna.html')

        new_account = Account(login=login, password=password, pochta=pochta)
        db.session.add(new_account)
        db.session.commit()

        flash('Account created successfully!', 'success')
        return redirect(url_for('glavna'))

    # Обработка GET-запроса (отображение игр и фильтрация)
    selected_genres = request.args.getlist('genre')

    games = Database.query.all()

    if selected_genres:
        filtered_games = []
        for game in games:
            game_tags = [game.teg1, game.teg2, game.teg3]
            for genre in selected_genres:
                if any(genre.lower() in str(tag).lower() for tag in game_tags if tag):
                    filtered_games.append(game)
                    break
        games = filtered_games

    return render_template('glavna.html', glavna=games, js_file=url_for('static', filename='главная.js'), css_file=url_for('static', filename='главня.css'))


@app.route('/karta1/<int:id>')
def karta1(id):
    karta1_item = Database.query.get_or_404(id)
    if karta1_item:
        items = [karta1_item]
        return render_template('karta1.html', items=items, css_file=url_for('static', filename='karta1.css'))
    else:
        flash('Номер не найден')
        return redirect(url_for('glavna'))  # Исправлено: перенаправление на главную


@app.route('/Profile/<int:user_id>')
def prof(user_id):
    profile_Database = Database.query.get(user_id)

    if profile_Database:
        items = [profile_Database]
        return render_template('Profile.html', items=items, css_file=url_for('static', filename='Profile.css'))
    else:
        flash('Профиль не найден')
        return redirect(url_for('glavna'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
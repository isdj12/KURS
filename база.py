from flask import Flask, redirect, url_for, flash, session, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '1'  # ОБЯЗАТЕЛЬНО ЗАМЕНИТЕ на надежный секретный ключ!
db = SQLAlchemy(app)


class Database(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    opis = db.Column(db.String(1000), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    teg1 = db.Column(db.String(50), nullable=False)
    teg2 = db.Column(db.String(50), nullable=True)
    teg3 = db.Column(db.String(50), nullable=True)
    image = db.Column(db.String(255), nullable=True)
    user_id db.Column(db.int(255), nullable=False)

    def __init__(id, self, opis, name, teg1, teg2=None, teg3=None, image=None):
        self.id = id
        self.opis = opis
        self.name = name
        self.teg1 = teg1
        self.teg2 = teg2
        self.teg3 = teg3
        self.image = image
        self.user_id = user_id


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def glavna():
    if request.method == 'POST':
        # Обработка формы добавления новой игры
        id = request.form.get('id')
        opis = request.form.get('opis')
        name = request.form.get('name')
        teg1 = request.form.get('teg1')
        teg2 = request.form.get('teg2')
        teg3 = request.form.get('teg3')
        image = request.form.get('image')
        user_id = request.form.get('user_id')


    # Обработка GET-запроса (отображение игр и фильтрация)
    selected_genres = request.args.getlist('genre')  # Получаем список выбранных жанров

    games = Database.query.all()  # По умолчанию показываем все игры

    if selected_genres:
        # Фильтруем игры по выбранным жанрам
        filtered_games = []
        for game in games:
            # Проверяем, соответствует ли хотя бы один тег игры выбранному жанру
            game_tags = [game.teg1, game.teg2, game.teg3]
            for genre in selected_genres:
                if any(genre.lower() in str(tag).lower() for tag in game_tags if tag):  #Проверяем, что тег не None
                    filtered_games.append(game)
                    break  # Переходим к следующей игре, если нашли соответствие
        games = filtered_games  # Обновляем список игр для отображения

    return render_template('glavna.html', glavna=games, css_file=url_for('static', filename='главня.css'))


@app.route('/karta1/<int:id>') #Убрал лишнюю запятую
def karta1(id):
    karta1_item = Database.query.get_or_404(id)
    if karta1_item:      
        items = [karta1_item]  
        return render_template('karta1.html', items = items, css_file=url_for('static',filename='karta1.css'))
    else:
        flash('Номер не найден')
        return redirect(url_for('home'))
    #--------------------------------------
@app.route('/Profile')
def prof():
    user_id = request.args.get('id')  # Get the 'id' from the URL
    if user_id:
        try:
            user_id = int(user_id)
            profile_acc = acc.query.get_or_404(user_id)  # Use user_id
            items = [profile_acc]
            return render_template('Profile.html', items=items, css_file=url_for('static', filename='Profile.css'))
        except ValueError:
            flash('Invalid ID')
            return redirect(url_for('glavna')) 
    else:
        flash('No ID provided')
      
    
    


if __name__ == '__main__':
    app.run(debug=True)
        

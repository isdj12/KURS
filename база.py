from flask import Flask, redirect, url_for, flash, session, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '1'  # ОБЯЗАТЕЛЬНО ЗАМЕНИТЕ на надежный секретный ключ!
db = SQLAlchemy(app)


class Database(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    opis = db.Column(db.String(1000), nullable=False)  # Увеличил длину, чтобы вместить описание
    name = db.Column(db.String(150), nullable=False)
    teg1 = db.Column(db.String(50), nullable=False) #Увеличил длину тегов
    teg2 = db.Column(db.String(50), nullable=True)
    teg3 = db.Column(db.String(50), nullable=True)
    image = db.Column(db.String(255), nullable=True) # Добавлено поле для хранения пути к изображению

    def __init__(self, opis, name, teg1, teg2=None, teg3=None, image=None):
        self.opis = opis
        self.name = name
        self.teg1 = teg1
        self.teg2 = teg2
        self.teg3 = teg3
        self.image = image


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def glavna():
    if request.method == 'POST':
        # Получаем данные из формы
        opis = request.form.get('opis')  # Используем .get() для безопасности
        name = request.form.get('name')
        teg1 = request.form.get('teg1')
        teg2 = request.form.get('teg2')
        teg3 = request.form.get('teg3')
        image = request.form.get('image') # Получение пути к изображению (если есть)

        # Валидация: проверяем, что обязательные поля заполнены
        if not opis or not name or not teg1:
            flash('Поля "Описание", "Название" и "Тег1" обязательны к заполнению.')
            return redirect(url_for('glavna'))

        # Создаем новый объект и добавляем в БД
        new_game = Database(opis=opis, name=name, teg1=teg1, teg2=teg2, teg3=teg3, image=image)
        db.session.add(new_game)
        try:
            db.session.commit()
            flash('Новая игра добавлена!')
        except Exception as e:
            db.session.rollback()  # Откатываем изменения в случае ошибки
            flash(f'Произошла ошибка при добавлении игры: {e}')
        return redirect(url_for('glavna'))

    # Получаем все записи из базы данных для отображения на странице
    games = Database.query.all()
    return render_template('glavna.html', glavna=games, css_file=url_for('static', filename='главня.css'))


if __name__ == '__main__':
    app.run(debug=True)
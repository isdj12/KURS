from flask import Flask, redirect, url_for, flash, session, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///database.db'
db = SQLAlchemy(app)

class Database(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    opis = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    
    def __init__(self, opis, name):
        self.opis = opis
        self.name = name
        
with app.app_context():
    db.create_all()
    
@app.route('/', methods=['GET', 'POST'])
def glavna():
    if request.method == 'POST':
        opis = request.form['opis']
        name = request.form['name']
        
        if len(opis) == 0 or len(name) == 0:
            flash('Opis i ime moraju biti uneti.')
            return redirect(url_for('glavna'))
        
        new_db = Database(opis, name)
        db.session.add(new_db)
        db.session.commit()
        flash('Novi podatak je dodat.')
        return redirect(url_for('glavna'))
    
    db_data = Database.query.all()
    return render_template('glavna.html', css_file=url_for('glavna.css'))

if __name__ == '__main__':
    app.run(debug=True)
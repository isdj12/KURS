from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/about')
def home():
    return render_template("index2.html")  # или index2.html, если вы хотите отрендерить index2.html по умолчанию

@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return "Привет, пользователь " + name + " с ID " + str(id)

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "Secret key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.app_context().push()


class Data(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def __init__(self, name, email, phone):

        self.name = name
        self.email = email
        self.phone = phone


with app.app_context():
    db.drop_all()


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    data = Data.query.all()      # put application's code here
    return render_template('index.html', employees=data)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        data = Data(name, email, phone)
        db.session.add(data)
        db.session.commit()

        flash("Данные добавлены")

        return redirect(url_for('index'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        data = Data.query.get(request.form.get('id'))

        data.name = request.form['name']
        data.email = request.form['email']
        data.phone = request.form['phone']

        db.session.commit()
        flash("Данные обновлены")

        return redirect(url_for('index'))


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    data = Data.query.get(id)
    db.session.delete(data)
    db.session.commit()
    flash("Данные удалены")

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

from flask import render_template, request, flash, redirect, url_for

from model import Data, app, db


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

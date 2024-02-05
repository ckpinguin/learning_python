from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, TimeField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = URLField('Location URL', validators=[DataRequired(), URL()])
    open_time = TimeField('Opening Time', validators=[DataRequired()])
    close_time = TimeField('Closing Time', validators=[DataRequired()])
    coffee_rating = SelectField(
        'Coffee Rating (0-5)', validators=[DataRequired()],
        choices=[(str(i), str(i)) for i in range(6)])
    wifi_rating = SelectField(
        'Wifi Rating (0-5)', validators=[DataRequired()],
        choices=[(str(i), str(i)) for i in range(6)])
    power_rating = SelectField(
        'Power Rating (0-5)', validators=[DataRequired()],
        choices=[(str(i), str(i)) for i in range(6)])
    submit = SubmitField('Submit')


def rating_coffee_to_emojis(rating):
    return '☕' * rating


app.jinja_env.filters['rating_coffee_to_emojis'] = rating_coffee_to_emojis


def rating_power_to_emojis(rating):
    return '🔌' * rating


app.jinja_env.filters['rating_power_to_emojis'] = rating_power_to_emojis


def rating_wifi_to_emojis(rating):
    return '💪' * rating


app.jinja_env.filters['rating_wifi_to_emojis'] = rating_wifi_to_emojis


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["post", "get"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('./cafe-data.csv', 'a', encoding='utf-8') \
                as csv_file:
            csv_writer = csv.writer(csv_file)
            new_row = [form.cafe.data, form.location.data,
                       form.open_time.data, form.close_time.data,
                       form.coffee_rating.data, form.wifi_rating.data,
                       form.power_rating.data]
            csv_writer.writerow(new_row)
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('./cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    print(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)

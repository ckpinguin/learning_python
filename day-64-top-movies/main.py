from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, desc
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, IntegerField, FloatField
from wtforms.validators import DataRequired, URL
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


# CREATE DB

class Base(DeclarativeBase):
    pass


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(model_class=Base)
migrate = Migrate(app, db)

db.init_app(app)

# CREATE TABLE


class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(
        String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()

""" new_movie = Movie(
    title="Phone Booth",
    year=2002,
    description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
    rating=7.3,
    ranking=10,
    review="My favourite character was the caller.",
    img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
)
second_movie = Movie(
    title="Avatar The Way of Water",
    year=2022,
    description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
    rating=7.3,
    ranking=9,
    review="I liked the water.",
    img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
)
with app.app_context():
    db.session.add(new_movie)
    db.session.add(second_movie)
    db.session.commit() """

# Create Forms


class AddMovieForm(FlaskForm):
    title = StringField('Movie title', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    rating = FloatField('Rating', validators=[DataRequired()])
    review = StringField('Review', validators=[DataRequired()])
    img_url = URLField('Image URL', validators=[DataRequired(), URL()])
    submit = SubmitField('Submit')


class EditRatingReviewForm(FlaskForm):
    rating = StringField("Your Rating Out of 10 e.g. 7.5")
    review = StringField("Your Review")
    submit = SubmitField("Done")


@app.route("/")
def home():
    all_movies = Movie.query.order_by(Movie.rating).all()
    # Update rankings for the movies
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template("index.html", movies=all_movies)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddMovieForm()
    if form.validate_on_submit():
        new_movie = Movie(title=form.title.data,
                          year=form.year.data,
                          description=form.description.data,
                          rating=form.rating.data,
                          ranking=form.ranking.data,
                          review=form.review.data,
                          img_url=form.img_url.data)
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html', form=form)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    form = EditRatingReviewForm()
    if form.validate_on_submit():
        movie_id = request.args.get("id")
        movie_to_update = db.get_or_404(Movie, movie_id)
        movie_to_update.rating = form.rating.data
        movie_to_update.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    if request.method == "GET":
        movie_id = request.args.get("id")
        movie_selected = db.get_or_404(Movie, movie_id)
        return render_template('edit.html', form=form, movie=movie_selected)


@app.route("/delete/", methods=["GET"])
def delete():
    movie_id = request.args.get("id")
    movie_to_delete = db.get_or_404(Movie, movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)

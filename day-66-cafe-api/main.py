from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, func

app = Flask(__name__)

# CREATE DB


class Base(DeclarativeBase):
    pass


# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        # dictionary = {}
        # for column in self.__table__.columns:
        #    dictionary[column.name] = getattr(self, column.name)
        # return dictionary

        # Method 2. Altenatively use Dictionary Comprehension to
        # do the same thing.
        return {column.name: getattr(self, column.name)
                for column in self.__table__.columns}


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random")
def get_random_cafe():
    # result = db.session.execute(db.select(Cafe))
    # all_cafes = result.scalars().all
    # More modern & concise is this:
    # all_cafes = Cafe.query.all()
    # More efficient to make the choice in db already:
    random_cafe = Cafe.query.order_by(func.random()).first()
    return jsonify(random_cafe.to_dict())


@app.route("/all")
def get_all_cafes():
    all_cafes = Cafe.query.all()
    list_of_cafes = [cafe.to_dict() for cafe in all_cafes]
    return jsonify(list_of_cafes)
    # return [jsonify(cafe.to_dict()) for cafe in all_cafes]


@app.route("/search")
def search_cafe():
    name = request.args.get('name')
    location = request.args.get('loc')
    matched_cafes = Cafe.query.filter(Cafe.name.like(
        f"%{name}%"), Cafe.location.like(f"%{location}%")).all()
    print(matched_cafes)
    print(Cafe.query.filter(Cafe.name.like(
        f"%{name}%"), Cafe.location.like(f"%{location}%")).statement)
    list_of_cafes = [cafe.to_dict() for cafe in matched_cafes]
    return jsonify(list_of_cafes)


if __name__ == '__main__':
    app.run(debug=True)

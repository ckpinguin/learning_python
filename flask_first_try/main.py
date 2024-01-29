from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def make_bold(function):
    def wrapper():
        return "<b>" + function() + "</b>"
    return wrapper


def make_emphasis(function):
    def wrapper():
        return "<em>" + function() + "</em>"
    return wrapper


def make_underlined(function):
    def wrapper():
        return "<u>" + function() + "</u>"
    return wrapper


def make_bold_with_args(function):
    def wrapper(*args, **kwargs):
        function(*args, **kwargs)
    return wrapper


@app.route("/bye")
@make_bold
@make_underlined
@make_emphasis
def bye():
    return "Bye!"


@app.route("/<name>/<int:number>")
@make_bold_with_args
def greet(name, number):
    return f"Hello there, {name}, {number}!"


if __name__ == "__main__":
    app.run(debug=True)

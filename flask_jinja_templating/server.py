from flask import Flask, render_template
import random
import requests

app = Flask(__name__)


@app.route('/')
def home():
    rand_num = random.randint(1, 10)
    return render_template('index.html', num=rand_num, year=2024, name="Jim")


@app.route('/guess/<name>')
def guess_name_age(name):
    response = requests.get(f'https://api.agify.io?name={name}')
    data = response.json()
    age = data["age"]
    return f"<p>You might be {age} years old."


if __name__ == "__main__":
    app.run(debug=True)

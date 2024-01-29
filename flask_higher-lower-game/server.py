from flask import Flask
import random

app = Flask(__name__)

rand_number = random.randint(0, 9)


@app.route("/")
def home():
    return "<h1>Guess a number between 0 and 9</h1>"\
        "<img src='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExM2xiYndmeXk1b3JxZmxxYjVid2gzZ3dmOHdodnk1cGJxdDN4aDJrbyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/6K0YmUf9EbUthpLxUu/giphy.gif' />"


@app.route("/<int:number>")
def greet(number):
    if number < rand_number:
        return f"<h1 style='color:red'>No! The number {number} is too low!</h1>" \
            "<img src='https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZDNta3JodHY3dWducmN6OHJyamN1bmM5enp4cnI2N282bGJxajRyaiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oz8xtd06ZcBwP4yFW/giphy.gif' />"
    elif number > rand_number:
        return f"<h1 style='color:orange'>No! The number {number} is too high!</h1>" \
            "<img src='https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExbHVraXhyeGUwN3liZXByNWR5cmZ5aW05ZjhoMW94bzJzMDNtNWZrOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l4JyUflefBVm82Pw4/giphy.gif' />"
    elif number == rand_number:
        return f"<h1 style='color: green'>Yes! The number {number} is correct!</h1>" \
            "<img src='https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExdW5hM2pvbmtodnJqcGUycXFlM3d3eW9jNHR5bHd5YnV3dGpxNTh4dyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3ohjUWwFJ9y81RO69q/giphy.gif' />"


if __name__ == "__main__":
    app.run(debug=True)

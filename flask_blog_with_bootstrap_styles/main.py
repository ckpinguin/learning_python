from flask import Flask, render_template
import requests

app = Flask(__name__)

blog_api = "https://api.npoint.io/0ec96b163952488a0881"


response = requests.get(blog_api)
posts: list[dict] = response.json()


@app.route("/")
def home():
    return render_template('index.html', posts=posts)


@app.route("/post/<id>")
def post(id):
    requestedPost = None
    for post in posts:
        if post["id"] == int(id):
            requestedPost = post
            print(requestedPost)

    return render_template('post.html', post=requestedPost)


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/contact")
def contact():
    return render_template('contact.html')


if __name__ == "__main__":
    app.run(debug=True)

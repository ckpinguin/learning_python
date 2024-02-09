from flask import Flask, render_template
import requests

from post import Post


app = Flask(__name__)

response = requests.get("https://api.npoint.io/a56ef48d075476a4188a")
data = response.json()
posts = [Post(title=post["title"],
              post_id=post["id"],
              subtitle=post["subtitle"],
              body=post["body"]) for post in data]


@app.route('/')
def home():
    print(posts)
    return render_template("index.html", posts=posts)


@app.route('/post/<int:id>')
def blog_post(id):
    requested_post = None
    for blog_post in posts:
        if blog_post.id == id:
            requested_post = blog_post

    if not requested_post:
        return "post_not_found."
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True)

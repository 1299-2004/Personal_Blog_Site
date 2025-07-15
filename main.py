from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

BLOG_FILE = "blog_posts.json"

# Load blog posts
def load_posts():
    if os.path.exists(BLOG_FILE):
        with open(BLOG_FILE, "r") as f:
            return json.load(f)
    return {}

# Save blog posts
def save_posts(posts):
    with open(BLOG_FILE, "w") as f:
        json.dump(posts, f, indent=4)

@app.route("/")
def index():
    posts = load_posts()
    return render_template("index.html", posts=posts)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        posts = load_posts()
        posts[title] = content
        save_posts(posts)
        return redirect(url_for("index"))
    return render_template("create.html")

@app.route("/edit/<title>", methods=["GET", "POST"])
def edit(title):
    posts = load_posts()
    if request.method == "POST":
        content = request.form["content"]
        posts[title] = content
        save_posts(posts)
        return redirect(url_for("index"))
    return render_template("edit.html", title=title, content=posts.get(title, ""))

@app.route("/delete/<title>")
def delete(title):
    posts = load_posts()
    posts.pop(title, None)
    save_posts(posts)
    return redirect(url_for("index"))

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


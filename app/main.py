from flask import Flask, render_template, abort
from dotenv import load_dotenv
from app.config import SOCIAL_LINKS
from app.blog_data import BLOG_POSTS

load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.context_processor
def inject_socials():
    return dict(social=SOCIAL_LINKS)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tools")
def tools():
    return render_template("tools.html")

@app.route("/classes")
def classes():
    return render_template("classes.html")

@app.route("/blog")
def blog():
    posts = sorted(BLOG_POSTS, key=lambda p: p["date"], reverse=True)
    return render_template("blog.html", posts=posts)

@app.route("/blog/<slug>")
def blog_post(slug):
    post = next((p for p in BLOG_POSTS if p["slug"] == slug), None)
    if not post:
        abort(404)
    return render_template("blog_post.html", post=post)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

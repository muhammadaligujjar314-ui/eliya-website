from flask import Flask, render_template, abort
from dotenv import load_dotenv
from app.config import SOCIAL_LINKS
from app.blog_data import BLOG_POSTS
import os
from groq import Groq

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

@app.route("/goals")
def goals():
    return render_templates("goals.html") 

@app.route("/goals/custom")
def goal_custom():
    return render_template("goal_custom.html")

@app.route("/goals/money")
def goal_money():
    return render_template("goal_money.html")

@app.route("/goals/schedule")
def goal_schedule():
    return render_template("goal_schedule.html")

@app.route("/goals/roadmap")
def goal_roadmap():
    return render_template("goal_roadmap.html")

@app.route("/goals/coding")
def coding_practice():
    return render_template("coding_practice.html")

@app.route("/api/generate-roadmap", methods=["POST"])
def generate_roadmap():
    from flask import request, jsonify
    goal = request.json.get("goal", "").strip()
    if not goal:
        return jsonify({"error": "Goal is required"}), 400

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return jsonify({"error": "Server not configured — missing GROQ_API_KEY"}), 500

    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{
                "role": "user",
                "content": f"Create a 30-day step-by-step roadmap to become a {goal}. "
                            f"Organize it into 4-5 weekly milestones, each with 3-4 short actionable daily tasks. "
                            f"Keep it practical and beginner-friendly. Format as plain text with clear headings."
            }],
            max_tokens=1200,
        )
        roadmap_text = response.choices[0].message.content
        return jsonify({"roadmap": roadmap_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
       

if __name__ == "__main__":
    app.run(debug=True, port=5000)

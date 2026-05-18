import json
from flask import Flask, render_template, request  # ← added 'request'

app = Flask(__name__)


def load_posts():
    """Read all blog posts from our JSON storage file."""
    with open('blog_posts.json', 'r') as f:
        return json.load(f)


@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])  # ← accepts BOTH request types
def add():
    if request.method == 'POST':
        # We will fill this in the next step
        pass
    return render_template('add.html')  # ← shown on GET (default)


if __name__ == '__main__':
    app.run(debug=True)
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


def load_posts():
    """Read all blog posts from our JSON storage file."""
    with open('blog_posts.json', 'r') as f:
        return json.load(f)


def save_posts(posts):
    """Write the updated list of posts back to our JSON storage file."""
    with open('blog_posts.json', 'w') as f:
        json.dump(posts, f, indent=4)  # indent=4 keeps the file neat & readable


@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        blog_posts = load_posts()  # 1. load existing posts

        # 2. grab each field from the submitted form
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        # 3. generate a unique ID (highest existing ID + 1)
        new_id = max(post['id'] for post in blog_posts) + 1 if blog_posts else 1

        # 4. build the new post as a dictionary
        new_post = {
            'id': new_id,
            'title': title,
            'author': author,
            'content': content
        }

        blog_posts.append(new_post)  # 5. add it to the list
        save_posts(blog_posts)  # 6. save updated list to JSON

        return redirect(url_for('index'))  # 7. send user back to home page

    return render_template('add.html')  # GET → just show the form


if __name__ == '__main__':
    app.run(debug=True)

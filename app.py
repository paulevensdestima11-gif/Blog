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
        json.dump(posts, f, indent=4)


@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        blog_posts = load_posts()

        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        new_id = max(post['id'] for post in blog_posts) + 1 if blog_posts else 1

        new_post = {
            'id': new_id,
            'title': title,
            'author': author,
            'content': content
        }

        blog_posts.append(new_post)
        save_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    blog_posts = load_posts()  # 1. load all posts

    # 2. keep every post EXCEPT the one with the matching id
    updated_posts = [post for post in blog_posts if post['id'] != post_id]

    save_posts(updated_posts)  # 3. save updated list

    return redirect(url_for('index'))  # 4. back to home!


if __name__ == '__main__':
    app.run(debug=True)
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


def fetch_post_by_id(post_id):
    """Find and return a single post by its ID, or None if not found."""
    blog_posts = load_posts()
    for post in blog_posts:
        if post['id'] == post_id:
            return post  # found it! return just this one post
    return None  # went through all posts, none matched


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
        new_post = {'id': new_id, 'title': title, 'author': author, 'content': content}
        blog_posts.append(new_post)
        save_posts(blog_posts)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    blog_posts = load_posts()
    updated_posts = [post for post in blog_posts if post['id'] != post_id]
    save_posts(updated_posts)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    post = fetch_post_by_id(post_id)  # fetch just this one post

    if post is None:
        return "Post not found", 404  # safety net — bad ID in URL

    if request.method == 'POST':
        blog_posts = load_posts()

        # loop through all posts and update the matching one
        for p in blog_posts:
            if p['id'] == post_id:
                p['title'] = request.form.get('title')
                p['author'] = request.form.get('author')
                p['content'] = request.form.get('content')

        save_posts(blog_posts)
        return redirect(url_for('index'))  # back to home after saving

    # GET request → show the form pre-filled with current post data
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(debug=True)
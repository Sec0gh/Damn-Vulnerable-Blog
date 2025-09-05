from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sqlite3, os, subprocess
from database import add_post, add_comment, get_comments, search_posts
from config import Config

post_bp = Blueprint('post', __name__)

@post_bp.route('/search')
def search():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    query = request.args.get('q', '').strip() 
    if query:
        posts = search_posts(query)
    else:
        posts = []
    
    return render_template('search.html', posts=posts, query=query)


@post_bp.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        add_post(title, content, session['user_id'])
        flash('Post created!', 'success')
        return redirect(url_for('dashboard.dashboard'))

    return render_template('create_post.html')


@post_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""
        SELECT posts.*, users.username, users.profile_photo 
        FROM posts 
        JOIN users ON posts.user_id = users.id 
        WHERE posts.id = ?""", (post_id,))
    post = c.fetchone()
    conn.close()

    if not post:
        flash('Post not found.', 'error')
        return redirect(url_for('dashboard.dashboard'))

    if request.method == 'POST':
        content = request.form['comment']
        add_comment(content, session['user_id'], post_id)
        flash('Comment added!', 'success')
        return redirect(url_for('post.view_post', post_id=post_id))

    comments = get_comments(post_id)
    return render_template('view_post.html', post=post, comments=comments)


@post_bp.route('/comment/<int:post_id>', methods=['POST'])
def add_comment_route(post_id):
    if 'user_id' not in session:
        flash('You must be logged in to comment.', 'error')
        return redirect(url_for('auth.login'))

    comment_text = request.form.get('comment_text')

    if not comment_text:
        flash('Comment cannot be empty.', 'error')
        return redirect(url_for('post.view_post', post_id=post_id))

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO comments (comment_text, user_id, post_id) VALUES (?, ?, ?)", 
              (comment_text, session['user_id'], post_id))
    conn.commit()
    conn.close()

    flash('Comment added successfully.', 'success')
    return redirect(url_for('post.view_post', post_id=post_id))


@post_bp.route('/my_posts.html')
def my_posts():
    username = request.args.get('username', '')
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, content 
        FROM posts 
        WHERE user_id = (SELECT id FROM users WHERE username=?)
    """, (username,))
    rows = cursor.fetchall()
    conn.close()

    posts = []
    for row in rows:
        post_id, title, content = row
        posts.append({
            "id": post_id,
            "title": title,
            "content": content,
            "preview_url": f"http://{Config.HOST}:{Config.PORT}/fetch?url=http://{Config.HOST}:{Config.PORT}/post/{post_id}"
        })

    real_count = len(posts)
    postsnumber = request.args.get('postsnumber')
    if not postsnumber:
        return redirect(url_for('post.my_posts', username=username, postsnumber=real_count))
    try:
        count_result = subprocess.check_output(f"echo {postsnumber}", shell=True, text=True).strip()
    except Exception as e:
        count_result = f"Error: {e}"

    return render_template("my_posts.html", username=username, posts=posts, count_result=count_result)

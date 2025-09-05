import sqlite3

# Initialize database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
             username TEXT, 
             email TEXT, 
             password TEXT, 
             phone TEXT,
             profile_photo TEXT)''')  
    
    c.execute('''CREATE TABLE IF NOT EXISTS posts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT,
                 content TEXT,
                 user_id INTEGER)''')

    c.execute('''CREATE TABLE IF NOT EXISTS comments (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             comment_text TEXT NOT NULL,
             user_id INTEGER,
             post_id INTEGER
             )''')    
    
    # Add some sample data if empty
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO users (username, email, password, phone) VALUES (?, ?, ?, ?)",
                  ('admin', 'admin@example.com', 'admin123', '1234567890'))
        c.execute("INSERT INTO users (username, email, password, phone) VALUES (?, ?, ?, ?)",
                  ('alice', 'alice@example.com', 'alice123', '0987654321'))
        c.execute("INSERT INTO users (username, email, password, phone) VALUES (?, ?, ?, ?)",
                  ('bob', 'bob@example.com', 'bob123', '76981234124'))
        
    c.execute("SELECT COUNT(*) FROM posts")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO posts (title, content, user_id) VALUES (?, ?, ?)",
                  ('First Post', 'This is the first blog post content.', 1))
        c.execute("INSERT INTO posts (title, content, user_id) VALUES (?, ?, ?)",
                  ('Second Post', 'This is the second blog post content.', 2))
        c.execute("INSERT INTO posts (title, content, user_id) VALUES (?, ?, ?)",
                  ('Third Post', 'This is the third blog post content.', 3))    
    conn.commit()
    conn.close()

init_db()

# ----------------------------------------------------------------------------------------------------

def get_user_by_id(user_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    return user

def get_posts():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""
        SELECT posts.*, users.username, users.profile_photo 
        FROM posts 
        JOIN users ON posts.user_id = users.id
    """)
    posts = c.fetchall()
    conn.close()
    return posts

def search_posts(query):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    sql = f"""
        SELECT posts.*, users.username 
        FROM posts 
        JOIN users ON posts.user_id = users.id 
        WHERE posts.title LIKE '%{query}%' OR posts.content LIKE '%{query}%'
        ORDER BY posts.id DESC
    """
    c.execute(sql)
    posts = c.fetchall()
    conn.close()
    return posts

def update_password(user_id, new_password):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE users SET password = ? WHERE id = ?", (new_password, user_id))
    conn.commit()
    conn.close()

def create_user(username, email, password, phone):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()    
    c.execute("INSERT INTO users (username, email, password, phone) VALUES (?, ?, ?, ?)", (username, email, password, phone))
    conn.commit()
    user_id = c.lastrowid
    conn.close()
    return user_id


def add_post(title, content, user_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO posts (title, content, user_id) VALUES (?, ?, ?)",
              (title, content, user_id))
    conn.commit()
    conn.close()


def add_comment(comment_text, user_id, post_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO comments (comment_text, user_id, post_id) VALUES (?, ?, ?)",
              (comment_text, user_id, post_id))
    conn.commit()
    conn.close()


def get_comments(post_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""
        SELECT comments.comment_text, users.username, users.profile_photo 
        FROM comments 
        JOIN users ON comments.user_id = users.id 
        WHERE comments.post_id = ?
    """, (post_id,))
    comments = c.fetchall()
    conn.close()
    return comments

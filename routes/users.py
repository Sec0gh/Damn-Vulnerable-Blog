from flask import Blueprint, render_template, redirect, url_for, session, flash
import sqlite3

user_bp = Blueprint('user', __name__)

@user_bp.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    if not session:
        return redirect(url_for('auth.login'))
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

    flash('User deleted successfully.', 'success')
    return redirect(url_for('user.manage_users'))


@user_bp.route('/manage_users')
def manage_users():
    if 'admin' not in session.get('username'):
        flash('You are not authorized to view this page.', 'error')
        return redirect(url_for('dashboard.dashboard'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email FROM users WHERE username != 'admin'")
    users = cursor.fetchall()
    conn.close()

    return render_template('manage_users.html', users=users)

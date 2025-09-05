from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sqlite3
from database import create_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']

        create_user(username, email, password, phone)
        flash('Registration successful!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        try:
            c.execute(query)
            user = c.fetchone()
        except Exception as e:
            conn.close()
            flash(f"SQL error: {e}", 'error')
            return redirect(url_for('auth.login'))

        if not user:
            try:
                c.execute(f"SELECT * FROM users WHERE username = '{username}'")
                user_check = c.fetchone()
                if not user_check:
                    flash('Invalid username.', 'error')
                else:
                    flash('Incorrect password.', 'error')
            except Exception as e:
                flash(f"SQL error during user check: {e}", 'error')
            conn.close()
            return redirect(url_for('auth.login'))
        session['username'] = username
        session['user_id'] = user[0]
        session['session_id'] = 1000 + user[0]
        conn.close()
        flash('Login successful!', 'success')
        return redirect(url_for('dashboard.dashboard'))

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('auth.login'))

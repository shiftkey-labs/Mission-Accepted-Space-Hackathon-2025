"""
Auth Routes
Contains authentication-related routes like login, logout, register, etc.
"""
from flask import render_template, request, flash, redirect, url_for
from app.auth import bp


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login page."""
    if request.method == 'POST':
        # TODO: Implement login logic
        flash('Login functionality not yet implemented', 'info')
        return redirect(url_for('main.index'))
    return render_template('auth/login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page."""
    if request.method == 'POST':
        # TODO: Implement registration logic
        flash('Registration functionality not yet implemented', 'info')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html')


@bp.route('/logout')
def logout():
    """User logout."""
    # TODO: Implement logout logic
    flash('Logged out successfully', 'success')
    return redirect(url_for('main.index'))

from app.Dashboard import bp
from flask import render_template, request, jsonify, send_from_directory, redirect, url_for

@bp.route('/')
def dashboard():
    return render_template('Dashboard/dashboard.html', title='Dashboard')
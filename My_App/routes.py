from My_App.app import app, db
from flask import render_template, request, redirect, url_for, flash

@app.route('/home')
def index():
    return render_template('index.html')


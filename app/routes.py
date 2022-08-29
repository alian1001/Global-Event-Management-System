from app import app, db
from flask import Flask, render_template, redirect, url_for, request, session
from werkzeug.urls import url_parse
from sqlalchemy import func, extract

@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html', title = 'Home')
# -*- coding: utf-8 -*-
from app import app
from flask import render_template

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


# -*- coding: utf-8 -*-
from app import app

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return "Hello, World!"



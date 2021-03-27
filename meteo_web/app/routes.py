# -*- coding: utf-8 -*-
from app import app
from flask import render_template
from app.models import *

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    meteost_all = meteostations.query.order_by(meteostations.name).all()
    return render_template('index.html', title="MyMeteo", meteost_all=meteost_all)


# -*- coding: utf-8 -*-
from app import app
from flask import render_template
from app.models import *


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    meteost_all = meteostations.query.order_by(meteostations.name).all()
    return render_template('index.html', title="MyMeteo", meteost_all=meteost_all)


@app.route('/meteostation/<int:meteo_id>', methods=['GET', 'POST'])
def meteostation(meteo_id):
    my_meteost = meteostations.query.filter(meteostations.id == meteo_id).first_or_404()
    meteost_data = temperature.query.filter(temperature.meteostation_id == meteo_id).order_by(temperature.date).all()
    return render_template('meteostation.html', title='Data',  meteost=my_meteost, meteost_data=meteost_data)



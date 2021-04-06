# -*- coding: utf-8 -*-
from app import app
from flask import render_template, request, redirect, url_for
from app.models import *
from app.forms import *

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = MeteostationForm()
    meteost_all = meteostations.query.order_by(meteostations.name).all()
    form.meteostation.choices = [(-1, "---")] + [(m.id, m.name) for m in meteost_all]

    if request.method == 'GET':
        return render_template('index.html', title="MyMeteo",  meteost_all=meteost_all, form=form)
    elif form.validate_on_submit():
        return redirect(url_for('index'))



@app.route('/meteostation/<int:meteo_id>', methods=['GET', 'POST'])
def meteostation(meteo_id):
    my_meteost = meteostations.query.filter(meteostations.id == meteo_id).first_or_404()
    meteost_data = temperature.query.filter(temperature.meteostation_id == meteo_id).order_by(temperature.date).all()
    return render_template('meteostation.html', title='Data',  meteost=my_meteost, meteost_data=meteost_data)


@app.route('/meteostation/map', methods=['GET', 'POST'])
def map_of_meteostations():
    return render_template('map_of_meteostations.html')

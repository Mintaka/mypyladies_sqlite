# -*- coding: utf-8 -*-
from app import app


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return '''
<html>
    <head>
        <title>Pyladies</title>
    </head>
    <body>
        <h1>Hello Pyladies!</h1>
    </body>
</html>'''


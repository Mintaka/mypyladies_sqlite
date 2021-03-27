from flask import Flask

app = Flask(__name__, static_folder="assets")

from app import routes
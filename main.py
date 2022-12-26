from flask import Flask
from orders import orders_pages

app = Flask(__name__)
app.register_blueprint(orders_pages)

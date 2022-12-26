from flask_restful import Api

from app.resources import Metrics, Order

api = Api(prefix="/orders")

api.add_resource(Order, "/<int:order_id>", "")
api.add_resource(Metrics, "/metrics")

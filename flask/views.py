from flask import request, jsonify
from flask.views import MethodView
import requests


lst = []
secondaries = [9001]


class MessageView(MethodView):

    def get(self):
        return jsonify({"messages": lst})

    def post(self):
        message = request.get_json().get("message")
        lst.append(message)

        for sec_port in secondaries:
            r = requests.post(f'http://localhost:{sec_port}/secondary', json={'rep_message': message})
            if r.status_code != 201:
                return jsonify({'description': 'Failed'}), 400
        return jsonify({'description': 'Success'}), 201

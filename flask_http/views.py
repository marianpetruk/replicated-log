import requests
from flask import request, jsonify
from flask.views import MethodView
from requests.exceptions import ReadTimeout

lst = []
secondaries = ["secondary-1", "secondary-2"]
PORT = 9001


class MessageView(MethodView):

    def get(self):
        return jsonify({"messages": lst})

    def error_400(self):
        return jsonify({'description': 'Failed'}), 400

    def post(self):
        message = request.get_json().get("message")
        lst.append(message)

        for domain in secondaries:
            try:
                # r = requests.post(f'http://{domain}:{PORT}/secondary', json={'rep_message': message}, timeout=1)  # for testing sleepy secondary
                r = requests.post(f'http://{domain}:{PORT}/secondary', json={'rep_message': message})
            except ReadTimeout:
                return self.error_400()
            if r.status_code != 201:
                return self.error_400()
        return jsonify({'description': 'Success'}), 201

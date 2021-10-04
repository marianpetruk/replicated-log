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

    @staticmethod
    def error_400():
        return jsonify({'description': 'Failed'}), 400

    def post(self):
        params = request.get_json()
        message = params.get("message")
        timeout = int(params.get("timeout", 0))

        lst.append(message)

        request_data = {
            "json": {'rep_message': message}
        }
        if timeout:
            request_data['timeout'] = timeout

        for domain in secondaries:
            try:
                r = requests.post(f'http://{domain}:{PORT}/secondary', **request_data)
            except ReadTimeout:
                return self.error_400()

            if r.status_code != 201:
                return self.error_400()

        return jsonify({'description': 'Success'}), 201

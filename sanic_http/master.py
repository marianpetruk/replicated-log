from sanic import Sanic
from sanic.response import json
import requests
from requests.exceptions import ReadTimeout


lst = []
secondaries = ["127.0.0.1"]
PORT=9001
app = Sanic("App Name")


def error_400():
    return json({'description': 'Failed'}), 400


@app.route("/")
async def get(request):
    return json({"messages": lst})


@app.route('/', methods=['POST'])
async def post(request):
    message = request.json.get("message")
    lst.append(message)

    for domain in secondaries:
        try:
            # r = requests.post(f'http://{domain}:{PORT}/secondary', json={'rep_message': message}, timeout=1)  # for testing sleepy secondary
            r = requests.post(f'http://{domain}:{PORT}/', json={'rep_message': message})
        except ReadTimeout:
            return error_400()
        if r.status_code != 201:
            return error_400()
    return json({'description': 'Success'}, status=201)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)

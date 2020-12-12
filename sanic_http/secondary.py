from sanic import Sanic
from sanic.response import json


lst = []
app = Sanic("App Name")


@app.route("/", methods=['GET'])
async def get(request):
    return json({"messages": lst})


@app.route("/", methods=['POST'])
async def post(request):
    # time.sleep(5) # for testing sleepy secondary
    rep_message = request.json.get("rep_message")
    lst.append(rep_message)
    return json({'description': 'Replication Success'}, status=201)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9001)

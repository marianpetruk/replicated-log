from sanic import Sanic
from sanic.response import json
import asyncio

lst = []
app = Sanic("App Name")


@app.route("/", methods=['GET'])
async def get(request):
    return json({"messages": lst})


@app.route("/", methods=['POST'])
async def post(request):
    await asyncio.sleep(10)  # TODO: for testing sleepy secondary
    # time.sleep(25) # for testing sleepy secondary
    rep_message = request.json.get("rep_message")
    lst.append(rep_message)
    return json({'description': 'Replication Success', 'status_code': 201}, status=201)  # TODO: fix double status code

@app.route('/health', methods=['GET'])
async def healthcheck(request):
    return json({"status": "OK"})




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9001)

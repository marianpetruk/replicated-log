from sanic import Sanic
from sanic.response import json
import asyncio

dct = {}
app = Sanic("App Name")


# k = 0 for test purposes


@app.route("/", methods=['GET'])
async def get(request):
    sorted_dct = dict(sorted(dct.items(), key=lambda item: item[0]))
    if len(sorted_dct) == 0:
        return json({"messages": []})

    for i in range(len(sorted_dct)):
        if i not in sorted_dct:
            i -= 1
            break

    messages = list(sorted_dct.values())

    return json({"messages": messages[:i + 1]})


@app.route("/", methods=['POST'])
async def post(request):
    # global k
    # await asyncio.sleep(10)  # for testing sleepy secondary
    # time.sleep(25) # for testing sleepy secondary

    rep_message = request.json.get("rep_message")
    key_ = list(rep_message.keys())[0]

    if int(key_) not in dct:
        # Test total order and retries:
        #
        # if int(key_) == 3 and k == 0:
        #     k += 1
        #     dct.update({int(key_)+1: "Z"})
        #
        #     Simulate internal error:
        #     return json({'description': 'Replication Success', 'status_code': 502}, status=502)  # TODO: fix double status code

        dct.update({int(key_): rep_message[key_]})
    return json({'description': 'Replication Success', 'status_code': 201}, status=201)  # TODO: fix double status code


@app.route('/health', methods=['GET'])
async def healthcheck(request):
    return json({"status": "OK"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9001)

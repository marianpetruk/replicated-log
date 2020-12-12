import requests
# from requests.exceptions import ReadTimeout
from sanic import Sanic
from sanic.response import json
# import aiohttp
from sync_tools import Notifier  # , CountDownLatch
# import threading
# import multiprocessing
# import asyncio
from gevent import monkey, sleep

# from greenlet import GreenletExit

monkey.patch_all()
# from gevent.queue import JoinableQueue
from gevent.pool import Pool
from gevent import joinall, killall

lst = []
# secondaries = ["127.0.0.1"]
secondaries = ["secondary-1", "secondary-2"]
PORT = 9001
# ports = [9001, 9002]
app = Sanic("App Name")


@app.route("/")
async def get(request):
    return json({"messages": lst})


def post_one(domain, message):
    r = requests.post(f'http://{domain}:{PORT}/', json={'rep_message': message})

    return r.status_code == 201


@app.route('/', methods=['POST'])
async def post(request):
    message = request.json.get("message")
    w = request.json.get("w") - 1
    lst.append(message)
    result = []
    num_of_ports = len(secondaries)
    pool = Pool(num_of_ports)
    notifier = Notifier(w, result, num_of_ports)

    gs = []
    for domain in secondaries:
        greenlet = pool.apply_async(post_one, kwds=dict(domain=domain, message=message),
                                    callback=notifier.accept_result)
        gs.append(greenlet)

    joinall(gs)

    while not result:
        continue
    if result[0]:
        return json({'description': 'Success'}, status=201)
    else:
        return json({'description': 'Fail'}, status=502)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)

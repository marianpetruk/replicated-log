import requests
# from requests.exceptions import ReadTimeout
from sanic import Sanic
from sanic.response import json
# import aiohttp
from sync_tools import Notifier, CountDownLatch
# import threading
# import multiprocessing
# import asyncio
from gevent import monkey, sleep

monkey.patch_all()
# from greenlet import GreenletExit

# from gevent.queue import JoinableQueue
from gevent.pool import Pool
from gevent import joinall, killall
import threading

lst = []
# secondaries = ["127.0.0.1"]
secondaries = ["secondary-1", "secondary-2"]
PORT = 9001
# ports = [9001, 9002]
app = Sanic("Master node")


@app.route("/")
async def get(request):
    return json({"messages": lst})


def post_one(cdl, domain, message):
    r = requests.post(f'http://{domain}:{PORT}/', json={'rep_message': message})
    if r.status_code == 201:
        cdl.count_down()
    return r.status_code == 201


@app.route('/', methods=['POST'])
async def post(request):
    message = request.json.get("message")
    write_concern = request.json.get("w")
    write_concern = len(secondaries) + 1 if write_concern is None else write_concern
    lst.append(message)
    # result = []
    # num_of_ports = len(secondaries)
    # pool = Pool(num_of_ports)
    # notifier = Notifier(write_concern - 1, result, num_of_ports)
    cdl = CountDownLatch(count=write_concern - 1)

    # gs = []
    for domain in secondaries:
        thread = threading.Thread(target=post_one, args=(cdl, domain, message))
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution

        # # greenlet = pool.apply_async(post_one, kwds=dict(domain=domain, message=message),
        # pool.apply_async(post_one, kwds=dict(domain=domain, message=message),
        #                             callback=notifier.accept_result)
        # gs.append(greenlet)

    if write_concern == 1:  # write concern 1 and therefore only master has to write the data
        return json({'description': 'Success'}, status=201)
    else:
        cdl.await_()
        # joinall(gs)
        # while not result:
        #     continue
        # if result[0]:
        #     print(f"result = {result}")
        #     return json({'description': 'Success'}, status=201)
        # else:
        #     return json({'description': 'Fail'}, status=502)
        return json({'description': 'Success'}, status=201)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, workers=2)

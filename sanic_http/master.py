import time

import requests
from requests.exceptions import ReadTimeout, ConnectionError
from sanic import Sanic
from sanic.response import json
import asyncio

from sync_tools import CountDownLatch

import threading

dct = {}
# id_ = 0
id_ = -1
# secondary_domain = "127.0.0.1"
secondaries = ["secondary-1", "secondary-2"]
PORT = 9001
ports = [9001, 9002]
app = Sanic("Master node")

# TODO rewrite to create dict dynamically
statuses = ["Healthy", "Suspected", "Unhealthy"]
secondaries_status = {"secondary-1": "Unhealthy", "secondary-2": "Unhealthy"}

secondaries_unsent = {"secondary-1": [], "secondary-2": []}

mode = "w"


@app.route("/")
async def get(request):
    return json({"messages": list(dict(sorted(dct.items(), key=lambda item: item[0])).values())})


def post_one(cdl, secondary_domain, message):
    try:
        r = requests.post(f'http://{secondary_domain}:{PORT}/', json={'rep_message': message}, timeout=5)
    except (ReadTimeout, ConnectionError):
        if secondaries_status[secondary_domain] != "Unhealthy":
            secondaries_status[secondary_domain] = statuses[statuses.index(secondaries_status[secondary_domain]) + 1]
        secondaries_unsent[secondary_domain].append(message)
        cdl.count_down()
        cdl.k = True
        # TODO check timeouted for master POST
        return False
    if r.status_code == 201:
        cdl.count_down()
    else:
        if secondaries_status[secondary_domain] != "Unhealthy":
            secondaries_status[secondary_domain] = statuses[statuses.index(secondaries_status[secondary_domain]) + 1]
        secondaries_unsent[secondary_domain].append(message)
        cdl.count_down()
        cdl.k = True
    return r.status_code == 201


def retry_request(secondary_domain, message):
    try:
        r = requests.post(f'http://{secondary_domain}:{PORT}/', json={'rep_message': message}, timeout=5)
    except (ReadTimeout, ConnectionError):
        if secondaries_status[secondary_domain] != "Unhealthy":
            secondaries_status[secondary_domain] = statuses[statuses.index(secondaries_status[secondary_domain]) + 1]
        return False
    if r.status_code == 201:
        secondaries_unsent[secondary_domain].remove(message)
    else:
        if secondaries_status[secondary_domain] != "Unhealthy":
            secondaries_status[secondary_domain] = statuses[statuses.index(secondaries_status[secondary_domain]) + 1]
    return True


def retry(secondary_domain):
    for unsent_message in secondaries_unsent[secondary_domain]:
        thread = threading.Thread(target=retry_request, args=(secondary_domain, unsent_message))
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution


def monitor_secondaries():
    while True:
        prev_statuses = secondaries_status.copy()

        for i in range(0, len(ports)):
            health_check_one(secondaries[i])
            if prev_statuses[secondaries[i]] != "Healthy" and secondaries_status[secondaries[i]] == "Healthy":
                retry(secondaries[i])

        time.sleep(10)


def health_check_one(secondary_domain):
    try:
        r = requests.get(f'http://{secondary_domain}:{PORT}/health', timeout=5)
        if r.status_code == 200:
            print(f"healthy {secondary_domain}")
            secondaries_status[secondary_domain] = "Healthy"
            return
    except (ReadTimeout, ConnectionError):
        pass

    if secondaries_status[secondary_domain] != "Unhealthy":
        secondaries_status[secondary_domain] = statuses[statuses.index(secondaries_status[secondary_domain]) + 1]
    else:
        secondaries_unsent[secondary_domain] = [{key: dct[key]} for key in dct]

@app.route('/', methods=['POST'])
async def post(request):
    global id_
    num_of_alive = list(secondaries_status.values()).count("Healthy")

    # We assume quorum is when at most one of secondaries is not present
    if len(secondaries) - num_of_alive > 1:
        mode = "ro"
    else:
        mode = "w"

    if mode == "ro":
        return json({'description': 'Some of secondaries are not available'}, status=502)

    # TODO return error if no message in request
    message = request.json.get("message")
    write_concern = request.json.get("w")
    write_concern = len(secondaries) + 1 if write_concern is None else write_concern
    id_ += 1
    dct[id_] = message

    while True:
        cdl = CountDownLatch(count=write_concern - 1)

        for i in range(0, len(ports)):
            thread = threading.Thread(target=post_one, args=(cdl, secondaries[i], {id_: message}))
            thread.daemon = True  # Daemonize thread
            thread.start()  # Start the execution

        # id_ += 1

        if write_concern == 1:  # write concern 1 and therefore only master has to write the data
            return json({'description': 'Success'}, status=201)
        else:
            cdl.await_()
            if cdl.k:
                await asyncio.sleep(30)
                continue

        return json({'description': 'Success'}, status=201)


@app.route('/health', methods=['GET'])
async def healthcheck(request):
    # thread_lists = []
    # for port in ports:
    #     thread = threading.Thread(target=health_check_one, args=(port,))
    #     thread.daemon = False  # Daemonize thread
    #     thread_lists.append(thread)
    #     thread.start() # Start the execution
    #
    # for thread in thread_lists:
    #     thread.join()

    return json({"status": secondaries_status})


if __name__ == "__main__":
    monitoring_thread = threading.Thread(target=monitor_secondaries)
    monitoring_thread.daemon = True
    monitoring_thread.start()

    app.run(host="0.0.0.0", port=9000, workers=1)

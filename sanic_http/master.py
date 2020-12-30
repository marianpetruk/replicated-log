import time

import requests
from requests.exceptions import ReadTimeout, ConnectionError
from sanic import Sanic
from sanic.response import json

from sync_tools import CountDownLatch

import threading

dct = {}
id_ = 0
secondary_domain = "127.0.0.1"
secondaries = ["secondary-1", "secondary-2"]
PORT = 9001
ports = [9001, 9002]
app = Sanic("Master node")

# TODO rewrite to create dict dynamically
statuses = ["Healthy", "Suspected", "Unhealthy"]
secondaries_status = {9001: "Healthy", 9002: "Healthy"}

secondaries_unsent = {9001: [], 9002: []}

mode = "w"


@app.route("/")
async def get(request):
    return json({"messages": list(dict(sorted(dct.items(), key=lambda item: item[0])).values())})


def post_one(cdl, port, message):
    try:
        r = requests.post(f'http://{secondary_domain}:{port}/', json={'rep_message': message}, timeout=5)
    except (ReadTimeout, ConnectionError):
        if secondaries_status[port] != "Unhealthy":
            secondaries_status[port] = statuses[statuses.index(secondaries_status[port]) + 1]
        secondaries_unsent[port].append(message)
        # TODO check timeouted for master POST
        return False
    if r.status_code == 201:
        cdl.count_down()
    else:
        if secondaries_status[port] != "Unhealthy":
            secondaries_status[port] = statuses[statuses.index(secondaries_status[port]) + 1]
        secondaries_unsent[port].append(message)
    return r.status_code == 201


def retry_request(port, message):
    try:
        r = requests.post(f'http://{secondary_domain}:{port}/', json={'rep_message': message}, timeout=5)
    except (ReadTimeout, ConnectionError):
        if secondaries_status[port] != "Unhealthy":
            secondaries_status[port] = statuses[statuses.index(secondaries_status[port]) + 1]
        return False
    if r.status_code == 201:
        secondaries_unsent[port].remove(message)
    else:
        if secondaries_status[port] != "Unhealthy":
            secondaries_status[port] = statuses[statuses.index(secondaries_status[port]) + 1]
    return True


def retry(port):
    for unsent_message in secondaries_unsent[port]:
        thread = threading.Thread(target=retry_request, args=(port, unsent_message))
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution


def monitor_secondaries():
    while True:
        prev_statuses = secondaries_status.copy()

        for port in ports:
            health_check_one(port)
            if prev_statuses[port] != "Healthy" and secondaries_status[port] == "Healthy":
                retry(port)

        time.sleep(30)


def health_check_one(port):
    try:
        r = requests.get(f'http://{secondary_domain}:{port}/health', timeout=5)
        if r.status_code == 200:
            secondaries_status[port] = "Healthy"
            return
    except (ReadTimeout, ConnectionError):
        pass

    if secondaries_status[port] != "Unhealthy":
        secondaries_status[port] = statuses[statuses.index(secondaries_status[port]) + 1]


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
    dct[id_] = message

    cdl = CountDownLatch(count=write_concern - 1)

    for port in ports:
        thread = threading.Thread(target=post_one, args=(cdl, port, {id_: message}))
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution

    id_ += 1

    if write_concern == 1:  # write concern 1 and therefore only master has to write the data
        return json({'description': 'Success'}, status=201)
    else:
        cdl.await_()

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
    # TODO find out how to share state between workers

    monitoring_thread = threading.Thread(target=monitor_secondaries)
    monitoring_thread.daemon = True
    monitoring_thread.start()

    app.run(host="0.0.0.0", port=9000, workers=1)

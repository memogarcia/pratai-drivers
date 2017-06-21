# -*- coding: utf-8 -*-

"""
driver.worker
~~~~~~~~~~~~~
This module connects to the cluster and starts polling messages from the queue
to be processed by docker
"""

import uuid

import zmq

from config import parse_config
import helpers
import cluster

receiver_endpoint = parse_config("queue")['receiver_endpoint']
sender_endpoint = parse_config("queue")['sender_endpoint']


def main():
    context = zmq.Context()
    worker = context.socket(zmq.PULL)
    worker.connect(receiver_endpoint)

    sender = context.socket(zmq.PUSH)
    sender.connect(sender_endpoint)

    daemon_id = uuid.uuid4().hex
    cluster.join(daemon_id, 'worker')
    print('Worker {0} running...'.format(daemon_id))

    try:

        # TODO(m3m0): make this loop aware of the resources in the host, so it can delay jobs.

        while True:
            work = worker.recv_json()
            action = work.get('action', None)
            payload = work.get('payload', None)
            request_id = work.get('request_id', None)
            function_id = work.get('function_id', None)
            image_id = work.get('image_id', None)

            if not action:
                continue

            if action == 'run':
                run_id = helpers.run(image_id, payload['payload'], function_id, request_id)

                sender.send_json({
                    "function_id": function_id,
                    "request_id": request_id,
                    "run_id": run_id.strip()
                })

            else:
                continue

    except (KeyboardInterrupt, Exception):
        pass

    finally:
        worker.close()
        sender.close()
        cluster.leave(daemon_id)

if __name__ == '__main__':
    main()

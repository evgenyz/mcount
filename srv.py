#!/usr/bin/env python3

import socket
import select

PORT = 50000


class Hub:
    def __init__(self):
        self._msg_counter = {}

    def put_message(self, did: str, msg: str):
        if did not in self._msg_counter:
            self._msg_counter[did] = 0
        self._msg_counter[did] += 1

    def __repr__(self):
        return "\n".join(["{}:\t{:d}".format(did, cnt) for did, cnt in self._msg_counter.items()]) if self._msg_counter else "None"


mhub = Hub()


srv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
srv.setblocking(False)
srv.bind(('localhost', PORT))

group = [srv]

while group:
    rd, wr, ex = select.select(group, [], group, 5.0)

    for s in rd:
        if s in group:
            data, addr = s.recvfrom(PORT)
            if data:
                try:
                    data = data.decode('utf-8')
                    did, msg = data.strip().split(" ", 1)
                    print("Got message ({}) from device {}".format(msg, did))
                    mhub.put_message(did, msg)
                except ValueError:
                    print("Bogus message: {!r}".format(data))

    for s in ex:
        print("Exceptional condition, terminating")
        if s in group:
            group.remove(s)
        s.close()
        break

    print("\nReceived messages:")
    print("{!r}\n".format(mhub))

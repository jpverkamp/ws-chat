#!/usr/bin/env python

import asyncio
import faker
import websockets

clients = []

fake = faker.Factory.create()

def broadcast(src, msg):
    for client in clients:
        if client.state == 'CLOSED':
            continue

        yield from client.send(src + ': ' + msg)

@asyncio.coroutine
def chat(client, path):
    name = fake.name()
    clients.append(client)
    yield from broadcast('server', name + 'has joined the chat')

    while True:
        msg = yield from client.recv()

        if msg:
            yield from broadcast(name, msg)
        else:
            break

    yield from broadcast('server', name + 'has left the chat')
    clients.remove(client)

start_server = websockets.serve(chat, '0.0.0.0', 9000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

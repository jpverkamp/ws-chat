#!/usr/bin/env python

import asyncio
import faker
import json
import websockets

clients = {}
fake = faker.Factory.create()

def broadcast(key, val):
    msg = json.dumps({key: val})

    for client_id, client in clients.items():
        if client['socket'].state == 'CLOSED':
            continue

        yield from client['socket'].send(msg)

@asyncio.coroutine
def chat(socket, path):

    client_id = fake.name()
    clients[client_id] = {
        'name': 'anonymous ' + client_id,
        'socket': socket,
    }

    yield from broadcast('hello', clients[client_id]['name'])

    while True:
        msg = yield from socket.recv()

        if msg:
            data = json.loads(msg)
            for k, v in data.items():

                if k == 'say':
                    yield from broadcast('say', {'name': clients[client_id]['name'], 'msg': v})

                elif k == 'name':

                    old_name = clients[client_id]['name']
                    clients[client_id]['name'] = v

                    yield from broadcast('name', {'old': old_name, 'new': v})

        else:
            break

    yield from broadcast('goodbye', clients[client_id]['name'])
    del clients[client_id]

start_server = websockets.serve(chat, '0.0.0.0', 9000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

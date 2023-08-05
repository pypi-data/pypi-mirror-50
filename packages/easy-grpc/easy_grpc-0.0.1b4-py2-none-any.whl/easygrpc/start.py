# -*- coding: utf-8 -*-

import asyncio
import sys
from grpclib.server import Server
from grpclib.client import Channel
import easygrpc


async def start_server():
    loop = asyncio.get_running_loop()
    await easygrpc.ainit()

    servers = []
    for server_name in easygrpc.grpc_server.keys():
        servers.append(
            easygrpc.attrs[f'{server_name}Impl'](easygrpc)
        )

    server = Server(servers, loop=loop)
    await server.start(easygrpc.grpc_host, easygrpc.grpc_port)

    print(f"""Easy GRPC Server
================
Status: LISTENING\nAddress: {easygrpc.grpc_host}:{easygrpc.grpc_port}
    """)

    try:
        await server.wait_closed()

    except asyncio.CancelledError:

        print("Closing server.")
        server.close()
        await server.wait_closed()

async def start_client(client = None):
    loop = asyncio.get_event_loop()
    await easygrpc.ainit()

    if len(easygrpc.grpc_client) == 0:
        print("Sorry, but you have not declared any client.")

    elif client is not None and client not in easygrpc.grpc_client.keys():
        print(f"Client {client} not exist, You can try one of the followings:")
        for key in easygrpc.grpc_client.keys():
            print(f" - {key}")

    else:

        channel = Channel(easygrpc.grpc_host, easygrpc.grpc_port, loop=loop)

        if client is None:
            # Get first
            c = easygrpc.grpc_client[
                list(easygrpc.grpc_client.keys())[0]
            ]
        else:
            # Get requested
            c = easygrpc.grpc_client[client]

        await c(channel)
        channel.close()

if __name__ == '__main__':
    if '-client' in sys.argv or '-c' in sys.argv:
        asyncio.run(
            start_client(
                sys.argv[2] if len(sys.argv) == 3 else None
            )
        )

    else:
        asyncio.run(start_server())

# -*- coding: utf-8 -*-

import importlib
import os
import configparser
import asyncio
import asyncpg
import inspect
from functools import (partial, wraps)
from .action import Action
from .state import State

attrs = {
    'grpc_server': {},
    'grpc_client': {},
    'grpc_server_function': None,
    'grpc_host': '127.0.0.1',  # can be overwritten with config file
    'grpc_port': 50051  # can be overwritten with config file
}

def init(config_file='./config.ini'):

    if os.path.isfile(config_file) is True:
        config = configparser.ConfigParser()
        config.read(config_file)

    else:
        raise Exception(f"Config file {config_file} not found.")

    global _state
    _state = State(config)

    ioloop = asyncio.get_event_loop()
    _state.set_connection(
        ioloop.run_until_complete(
            asyncpg.create_pool(**config['POSTGRESQL'])
        )
    )

    if 'ACTIONS' in config.sections():
        for key in config['ACTIONS']:
            name = key if '.' not in key else key.replace('.', '_')
            exec(f"""
def {name}(*arg, **args):
    act = _state.actions['{name}']
    ioloop = asyncio.get_event_loop()
    conn = None
    if _state.conn is not None:
        conn = ioloop.run_until_complete(
            _state.conn.acquire()
        )
    try:
        action = act(conn)
        result = ioloop.run_until_complete(
            action.process(*arg, **args)
        )
    finally:
        ioloop.run_until_complete(
            _state.conn.release(conn)
        )
    return result
            """, globals(), attrs)

async def ainit(config_file='./config.ini'):

    if os.path.isfile(config_file) is True:
        config = configparser.ConfigParser()
        config.read(config_file)

    else:
        raise Exception(f"Config file {config_file} not found.")

    global _state
    _state = State(config)

    # Init database connection
    if 'POSTGRESQL' in config.sections():
        _state.set_connection(
            (
                await asyncpg.create_pool(**config['POSTGRESQL'])
            )
        )

    # prepare the server initialization
    if 'SERVER' in config.sections() and 'server' in config['SERVER']:

        if 'host' in config['SERVER']:
            attrs['grpc_host'] = config['SERVER']['host']
        if 'port' in config['SERVER']:
            attrs['grpc_port'] = int(config['SERVER']['port'])

        if 'client' in config['SERVER']:
            clients = [x.strip() for x in config['SERVER']['client'].split(',')]
            for client in clients:
                attrs['grpc_client'][client] = _state.import_action(
                    client
                )

        servers = [x.strip() for x in config['SERVER']['server'].split(',')]
        for server in servers:
            server_name = server.split('.')[-1]
            declared_server = _state.import_action(f'{server}Base')
            attrs['grpc_server'][server_name] = {
                'class': declared_server,
                'grpc_server_function': [],
                'str': f"""
class {server_name}Impl(attrs['grpc_server']['{server_name}']['class']):
    def __init__(self, easy):
        super().__init__()
        self.easy = easy
        """
            }

            # Create the GRPC Server Class
            methods = inspect.getmembers(
                declared_server,
                predicate=inspect.isfunction
            )

            for method in methods:
                if method[0] != '__mapping__':
                    attrs['grpc_server'][server_name][
                        'grpc_server_function'
                    ].append(method[0])

    if 'ACTIONS' in config.sections():
            
        for key in config['ACTIONS']:
            name = key if '.' not in key else key.replace('.', '_')
            exec(f"""
async def {name}(*arg, **args):
    act = _state.actions['{name}']
    if _state.conn is not None:
        async with _state.conn.acquire() as conn:
            action = act(conn)
            return (
                await action.process(*arg, **args)
            )
    else:
        action = act()
        return (
            await action.process(*arg, **args)
        )
            """, globals(), attrs)

        if (
            len(attrs['grpc_server'].keys()) > 0
        ):
            akeys = config['ACTIONS'].keys()
            for server_name in attrs['grpc_server'].keys():
                server = attrs['grpc_server'][server_name]
                for function in server['grpc_server_function']:
                    if function in akeys:
                        server['str'] += f'''
    async def {function}(self, stream):
        f = await stream.recv_message()
        await stream.send_message(
            await self.easy.{function.lower()}(f)
        )
'''
                    elif f'{server_name}.{function}' in akeys:
                        function_name = f'{server_name}_{function}'
                        server['str'] += f'''
    async def {function}(self, stream):
        f = await stream.recv_message()
        await stream.send_message(
            await self.easy.{function_name.lower()}(f)
        )
'''
                    else:
                        server['str'] += f'''
    async def {function}(self, stream):
        print("Not implemented")
        pass
                        '''

            for server_name in attrs['grpc_server'].keys():
                server = attrs['grpc_server'][server_name]
                # print(server)
                # print(server['str'])
                exec(server['str'], globals(), attrs)


# PEP 562 (customization of module attribute access)
def __dir__():
    keys = [
        'Action',
        'init',
        'grpc_server',
        'Query',
        'Id',
        'Where'
    ] + list(attrs.keys())
    keys.sort()
    return keys


def __getattr__(key):
    return attrs.get(key)


def __setattr__(key, value):
    attrs[key] = value

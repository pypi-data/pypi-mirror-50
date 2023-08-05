# Easy GRPC

Python (>=3.7) GRPC service helper library.

## Installation

We suggest to create a virtual environment.

```bash
python3.7 -m venv ./venv
source venv/bin/activate
python  -m pip install --upgrade pip
```

Install the module:

```bash
pip install easy-grpc

```

## Usage example

Easy GRPC helps you to create a GRPC Service in three steps:

1. Define and compile your proto files
2. Implement the *Actions*
3. Configure and run the GRPC service

### 1. Define and compile your proto files

In the example folder there are some files extracted from the [grpclib](https://github.com/vmagamedov/grpclib) repository, which is currently used to run this service. You can find the *helloworld.proto* and the relative compiled python files (*helloworld_pb2.py* and *helloworld_grpc.py*).

```protobuf
syntax = "proto3";

package example.helloworld;

message HelloRequest {
  string name = 1;
}

message HelloReply {
  string message = 1;
}

service Greeter {
  rpc SayHello (HelloRequest) returns (HelloReply) {}
}

```

To define the service you have to create the proto files as explained in the official documentations [grpc.io](https://grpc.io/docs/guides/concepts/).

To compile a proto file by yourself, just execute this command from the root directory.

```bash
python -m grpc_tools.protoc \
  --proto_path=. \
  --python_out=. \
  --python_grpc_out=. \
  ./example/helloworld.proto
```

> **Note:** pay attention to the *python_grpc_out* param. This is not standard in the *grpc_tools.protoc* library, it is [grpclib specific](https://grpclib.readthedocs.io/en/latest/index.html?highlight=python_grpc_out#protoc-plugin).

### 2. Implement the *Actions*

In the helloworld.proto file there is declared one rpc function (you can declare more). You shall create an action for each rpc, handling the defined input message (HelloRequest) and returning the relative return message (HelloReply).

In the case of the example the helloworld_action.py is created:

```python
from easygrpc import Action
from .helloworld_pb2 import  HelloReply


class Hello(Action):
    async def execute(self, hello_request=None):
        return HelloReply(message=f'Hello {hello_request.name}!')

```

An *Action* is a Class extending the **easygrpc.action.Action** abstract base class, and must overwrite the execute method.

### 3. Configure and run the GRPC service

Finally to run the service you shall create a config file which is used to configure and run the service.

```ini
[SERVER]
server = example.helloworld_grpc.GreeterBase
client = example.client.SendRequest
host = 127.0.0.1
port = 50051

[ACTIONS]
SayHello = example.helloworld_action.Hello

```

In the *ACTIONS* section you shall declare one action for each rcp function. Of corse you can declare more then the defined rpc that can be used and exposed.

To run the service just open a terminal, and:

```bash
source venv/bin/activate
python -m easygrpc.start
```

To execute the client, open another teminal, and:

```bash
source venv/bin/activate
python -m easygrpc.start -c
```

You should see the response from the service:

```bash
Hello Mr. Easy!
```


## Database interaction

In every implemented Action you have access to a PostgreSQL Database Client Library ([asyncpg](https://github.com/MagicStack/asyncpg)). In the config file, you define the PostgreSQL connection parameters. And the in the action implementation you can execute SQL commands to interact with the database.

create a postgreSQL (versions 9.2 to 10) database named 'easy'.

```bash
sudo -u postgres createdb -E UTF8 easy
```

Then create a new table:

```SQL
CREATE TABLE public.messages
(
    id serial,
    text character varying,
    PRIMARY KEY (id)
);
```

And insert a row:

```SQL
INSERT INTO public.messages(text) VALUES ('Hello PostgreSQL!');
```

Add the following configuration section:

```ini
[POSTGRESQL]
user = postgres
password = postgres
database = easy
host = localhost
port = 5432

```

Modify the Hello Action (example/helloword_action.py):

```python
from easygrpc import Action
from .helloworld_pb2 import  HelloReply


class Hello(Action):
    async def execute(self, hello_request=None):
        rec = await self.conn.fetchval("""
            SELECT row_to_json(t)
            FROM (
                SELECT
                    text as message
                FROM public.messages
                WHERE
                    id = $1
            ) as t
        """, 1)
        if rec is not None:
            return self.encode(rec, HelloReply)
        return None

```

To run the service just open a terminal, and:

```bash
source venv/bin/activate
python -m easygrpc.start
```

To execute the client, open another teminal, and:

```bash
source venv/bin/activate
python -m easygrpc.start -c
```


## Example with multiple Services

You can of course declare more then one service and clients in your proto file:


```protobuf
syntax = "proto3";

package example.helloworld;

message HelloRequest {
  string name = 1;
}

message HelloReply {
  string message = 1;
}

service Greeter {
  rpc SayHello (HelloRequest) returns (HelloReply) {}
}

service GreeterDB {
  rpc SayHello (HelloRequest) returns (HelloReply) {}
}

```

In this case the *config.ini* file will be a little bit different:

```ini
[POSTGRESQL]
user = postgres
password = postgres
database = easy
host = localhost
port = 5432

[SERVER]
server = example.helloworld_grpc.Greeter,
    example.helloworld_grpc.GreeterDB
client = example.client.SendRequest,
    example.client.SendRequestDb
host = 127.0.0.1
port = 50051

[ACTIONS]
Greeter.SayHello = example.helloworld_action.Hello
GreeterDB.SayHello = example.helloworld_action.HelloDb

```

Pay attention to the *ACTIONS* section. The keys are defined using a dot notation to identify which server is used with the given action.

The clients can also be more than one (see ./example/client.py):


```python
import asyncio

from grpclib.client import Channel

# generated by protoc
from .helloworld_pb2 import HelloRequest, HelloReply
from .helloworld_grpc import GreeterStub, GreeterDBStub


async def SendRequest(channel):
    greeter = GreeterStub(channel)

    reply = await greeter.SayHello(HelloRequest(name='Mr. Easy'))
    print(reply.message)

    channel.close()

async def SendRequestDb(channel):
    greeter = GreeterDBStub(channel)

    reply = await greeter.SayHello(HelloRequest(name='Mr. PostgreSQL'))
    print(reply.message)

    channel.close()
```

To run the service is just same as starting a single service instance:

```bash
source venv/bin/activate
python -m easygrpc.start
```

To execute the client, instead, you can chose which client to run:

```bash
source venv/bin/activate
python -m easygrpc.start -c example.client.SendRequestDb
```

> **Note:** *If the client is not give as a the parameter than the first one is executed*


 

# -*- coding: utf-8 -*-

import abc
import json
from google.protobuf.json_format import Parse,  MessageToJson
import time
try:
    from istsosproto import qry
except ImportError:
    qry = None


class Action(abc.ABC):

    fields = {}

    def __init__(self, conn=None):
        if qry is not None:
            self.parser = qry(self.fields)
        else:
            self._idx = 0
        self.conn = conn
        self.time = None

    def encode(self, data, proto):
        """Encode the given data (text or JSON) into the given
        proto message
        """
        return Parse(data, proto())

    def decode(self, proto):
        """Convert the given proto message in JSON
        """
        return MessageToJson(proto)

    @abc.abstractmethod
    async def execute(self, *arg, **args):
        raise NotImplementedError

    async def process(self, *arg, **args):
        start = time.time()
        result = await self.execute(*arg, **args)
        self.time = time.time() - start
        print("%s: %s Bytes in %s ms" % (
            self.__class__.__name__,
            result.ByteSize() if result is not None else '0',
            self.time * 1000
        ))
        return result

    def get_condition(self, where, prepend = None):
        if qry is not None:
            return self.parser.get_conditions(where, prepend)
        raise Exception(
            "To use get_condition function "
            "please install 'istsosproto' module"
        )

    def getIdx(self):
        if qry is not None:
            return self.parser.getIdx()
        self._idx += 1
        return "$%s" % self._idx

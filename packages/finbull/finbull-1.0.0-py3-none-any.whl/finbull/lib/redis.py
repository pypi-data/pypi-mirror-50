# -*- coding: utf-8 -*-
# Copyright (c) 2019 hcyjs.com, Inc. All Rights Reserved

import random
import time

import tornadis
import tornado.gen
import tornado.ioloop
import finbull.error
import finbull.log


class RedisDB(object):
    """
    RedisDB
    """
    # client number in connect pool
    MAX_CLIENT_CLIENT = 20
    RETRY_TIMES = 3

    def __init__(self, ip_list=None, consts=None, **client_kwargs):
        """
        init and connect at first time
        """
        self.client_kwargs = client_kwargs
        self.consts = consts or {}
        self.ip_list = ip_list

        if self.ip_list is None:
            raise finbull.error.BaseError(
                errno=finbull.error.ERRNO_FRAMEWORK,
                errmsg="finbull is empty both."
            )

        if not isinstance(self.ip_list, list):
            self.ip_list = [self.ip_list]
        self.pool = None

        # connect at first time
        tornado.ioloop.IOLoop.current().run_sync(self.restart_pool)

    @tornado.gen.coroutine
    def restart_pool(self):
        """start a connect pool

        Returns:
            TYPE: Description
        """
        if self.pool is not None:
            self.pool.destory()
        address = random.choice(self.ip_list)
        (ip, port) = address.split(":")
        self.pool = tornadis.ClientPool(
            max_size=self.MAX_CLIENT_CLIENT,
            host=ip,
            port=int(port),
            **self.client_kwargs)

    @tornado.gen.coroutine
    def _get_connected_client(self):
        """
        get a connected client from the pool
        if I can not find any client in the pool
        raise the `finbull.error.BaseError`
        """
        for i in range(0, self.RETRY_TIMES):
            client = yield self.pool.get_connected_client()
            if isinstance(client, tornadis.exceptions.ClientError):
                yield self.restart_pool()
            else:
                raise tornado.gen.Return(client)

        raise finbull.error.BaseError(
            errno=finbull.error.ERRNO_FRAMEWORK,
            errmsg="no redis can be connected."
        )

    @tornado.gen.coroutine
    def get(self, key):
        """Summary

        Args:
            key (TYPE): Description

        Returns:
            TYPE: Description
        """
        _start = int(round(time.time() * 1000))
        client = yield self._get_connected_client()
        result = yield client.call("GET", key)
        self.pool.release_client(client)
        _stop = int(round(time.time() * 1000)) - _start

        finbull.log.service_debug({
            "redis_log": "redis requested",
            "method": "GET",
            "key": key,
            "result": result,
            "time": _stop,
        })
        finbull.log.service_notice({
            "redis_log": "redis requested",
            "method": "GET",
            "key": key,
            "time": _stop,
        })
        raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def set(self, key, value, cache_time=None):
        """Summary

        Args:
            key (TYPE): Description

        Returns:
            TYPE: Description
        """
        _start = int(round(time.time() * 1000))
        client = yield self._get_connected_client()
        if cache_time is not None:
            result = yield client.call("SET", key, value, "EX", cache_time)
        else:
            result = yield client.call("SET", key, value)
        self.pool.release_client(client)
        _stop = int(round(time.time() * 1000)) - _start

        finbull.log.service_debug({
            "redis_log": "redis requested",
            "method": "SET",
            "key": key,
            "value": value,
            "result": result,
            "time": _stop,
        })
        finbull.log.service_notice({
            "redis_log": "redis requested",
            "method": "SET",
            "key": key,
            "time": _stop,
        })
        raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def zadd(self, key, valuelist):
        """add

        Args:
            key (TYPE): Description
            valuelist (TYPE): Description

        Returns:
            TYPE: Description

        Raises:
            gen.Return: Description
        """
        if isinstance(valuelist, list):
            valuelist = map(str, valuelist)

        _start = int(round(time.time() * 1000))
        client = yield self._get_connected_client()
        result = yield client.call("ZADD", key, *valuelist)
        self.pool.release_client(client)
        _stop = int(round(time.time() * 1000)) - _start

        finbull.log.service_debug({
            "redis_log": "redis requested",
            "method": "ZADD",
            "key": key,
            "value": valuelist,
            "result": result,
            "time": _stop,
        })
        finbull.log.service_notice({
            "redis_log": "redis requested",
            "method": "ZADD",
            "key": key,
            "time": _stop,
        })
        raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def zrevrange(self, key, count, withscores=False):
        """range

        Args:
            key (TYPE): Description
            valuelist (TYPE): Description

        Returns:
            TYPE: Description

        Raises:
            gen.Return: Description
        """
        _start = int(round(time.time() * 1000))
        client = yield self._get_connected_client()
        result = yield client.call("ZREVRANGE", key, 0, count - 1)
        self.pool.release_client(client)
        _stop = int(round(time.time() * 1000)) - _start

        finbull.log.service_debug({
            "redis_log": "redis requested",
            "method": "ZREVRANGE",
            "key": key,
            "result": result,
            "time": _stop,
        })
        finbull.log.service_notice({
            "redis_log": "redis requested",
            "method": "ZREVRANGE",
            "key": key,
            "time": _stop,
        })
        raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def sadd(self, key, valuelist):
        """add

        Args:
            key (TYPE): Description
            valuelist (TYPE): Description

        Returns:
            TYPE: Description

        Raises:
            gen.Return: Description
        """
        if isinstance(valuelist, list):
            valuelist = map(str, valuelist)

        _start = int(round(time.time() * 1000))
        client = yield self._get_connected_client()
        result = yield client.call("SADD", key, *valuelist)
        self.pool.release_client(client)
        _stop = int(round(time.time() * 1000)) - _start

        finbull.log.service_debug({
            "redis_log": "redis requested",
            "method": "SADD",
            "key": key,
            "value": valuelist,
            "result": result,
            "time": _stop,
        })
        finbull.log.service_notice({
            "redis_log": "redis requested",
            "method": "SADD",
            "key": key,
            "time": _stop,
        })
        raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def smembers(self, key):
        """sdiff

        Args:
            *keys (TYPE): Description

        Returns:
            TYPE: Description

        Raises:
            gen.Return: Description
        """
        _start = int(round(time.time() * 1000))
        client = yield self._get_connected_client()
        result = yield client.call("SMEMBERS", key)
        self.pool.release_client(client)
        _stop = int(round(time.time() * 1000)) - _start

        finbull.log.service_debug({
            "redis_log": "redis requested",
            "method": "SMEMBERS",
            "key": key,
            "result": result,
            "time": _stop,
        })
        finbull.log.service_notice({
            "redis_log": "redis requested",
            "method": "SMEMBERS",
            "key": key,
            "time": _stop,
        })
        raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def delete(self, keys):
        """delete

        Args:
            keys (TYPE): Description

        Returns:
            TYPE: Description

        Raises:
            gen.Return: Description
        """
        if not isinstance(keys, list):
            keys = [keys]

        _start = int(round(time.time() * 1000))
        client = yield self._get_connected_client()
        result = yield client.call("DEL", *keys)
        self.pool.release_client(client)
        _stop = int(round(time.time() * 1000)) - _start

        finbull.log.service_debug({
            "redis_log": "redis requested",
            "method": "DELETE",
            "key": key,
            "result": result,
            "time": _stop,
        })
        finbull.log.service_notice({
            "redis_log": "redis requested",
            "method": "DELETE",
            "key": key,
            "time": _stop,
        })
        raise tornado.gen.Return(result)

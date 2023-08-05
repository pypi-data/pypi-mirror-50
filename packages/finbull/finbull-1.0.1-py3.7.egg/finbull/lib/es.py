# -*- coding: utf-8 -*-
# Copyright (c) 2019 hcyjs.com, Inc. All Rights Reserved

import gzip
import io
import random
import time

import tornado.escape
import tornado.gen
import tornado.httpclient

import finbull.error
import finbull.log


class ElasticSearchDB(object):
    """Summary

    Attributes:
        addresses (list): Description
        client_type (str): Description
        index (TYPE): Description
        password (TYPE): Description
        type (TYPE): Description
        username (TYPE): Description
    """

    RETRY_TIMES = 3
    REQUEST_TIMEOUT = 2

    def __init__(self, ip_list=None, consts=None, **kwargs):
        self.addresses = []
        self.consts = consts or {}
        self.ip_list = ip_list

        if self.ip_list is None:
            raise finbull.error.BaseError(
                errno=finbull.error.ERRNO_FRAMEWORK,
                errmsg="ip_list is empty both."
            )

        if not isinstance(self.ip_list, list):
            self.ip_list = [self.ip_list]

        if "index" in kwargs:
            self.index = kwargs["index"]
        else:
            raise finbull.error.BaseError(
                errno=finbull.error.ERRNO_FRAMEWORK,
                errmsg="can not find index in service.conf"
            )

        self.username = kwargs["username"] if "username" in kwargs else ""
        self.password = kwargs["password"] if "password" in kwargs else ""

    def get_client(self):
        """Summary

        Returns:
            TYPE: Description
        """
        if self.ip_list is not None:
            server = random.choice(self.ip_list)
            (ip, port) = server.split(":")
            return "http://%s:%s/%s" % (ip, port, self.index)
        else:
            raise finbull.error.BaseError(
                errno=finbull.error.ERRNO_FRAMEWORK,
                errmsg="ElasticSearch Server Ip List Error"
            )

    @tornado.gen.coroutine
    def query(self, body, option="_search"):
        """query interface

        Args:
            body (dict): json body
            **kwargs (dict): params

        Returns:
            dict: json string

        Raises:
            gen.Return: Description
        """
        client = tornado.httpclient.AsyncHTTPClient()

        url = self.get_client()
        if option != "_msearch":
            body = tornado.escape.json_encode(body)

        for i in range(self.RETRY_TIMES):
            _start = int(round(time.time() * 1000))
            response = yield client.fetch(
                url + "/%s" % option,
                raise_error=False,
                method="POST",
                body=self._gzip_data(body),
                headers={"Content-Encoding": "gzip", "Content-Type": "application/gzip"},
                auth_username=self.username,
                auth_password=self.password,
                allow_nonstandard_methods=True,
                request_timeout=self.REQUEST_TIMEOUT
            )
            _stop = int(round(time.time() * 1000)) - _start
            # if the `raise_error` set to False in `client.fetch`
            # the response will always be returned regardless of the response code.
            # if the server return HTTP code,
            # maybe the server or the configuration is error.
            # so we do not retry.
            # error code 599 is used when no HTTP response was received, e.g. for a timeout.
            # so we retry when HTTP code is 599
            if response.code == 599:
                finbull.log.service_warning({
                    "finbull.lib.es": "es requested timeout",
                    "url": url,
                    "http_code": response.code,
                    "time": _stop,
                    "retry": "%d/%d" % (i + 1, self.RETRY_TIMES),
                })
                continue
            else:
                finbull.log.service_debug({
                    "finbull.lib.es": "es requested",
                    "url": url,
                    "req": body,
                    "res": response.body,
                    "http_code": response.code,
                    "time": _stop,
                    "retry": "%d/%d" % (i + 1, self.RETRY_TIMES),
                })
                finbull.log.service_notice({
                    "finbull.lib.es": "es requested",
                    "url": url,
                    "http_code": response.code,
                    "time": _stop,
                    "retry": "%d/%d" % (i + 1, self.RETRY_TIMES),
                })
                result = tornado.escape.json_decode(response.body).get("responses", [])
                raise tornado.gen.Return(result)

        finbull.log.service_warning({
            "finbull.lib.es": "can not request the elasticsearch",
            "url": url,
            "retry_times": self.RETRY_TIMES,
        })
        raise tornado.gen.Return([])

    @tornado.gen.coroutine
    def multi_query(self, bodies):
        """
        multi query
        """
        body = "\n".join(["\n".join([tornado.escape.json_encode(h),
                                     tornado.escape.json_encode(b)]) for h, b in bodies]) + "\n"
        result = yield self.query(body, option="_msearch")
        raise tornado.gen.Return(result)

    def _gzip_data(self, content):
        """
        compress the request data and response data.
        """
        zbuf = io.StringIO()
        zfile = gzip.GzipFile(mode='wb', compresslevel=9, fileobj=zbuf)
        zfile.write(content)
        zfile.close()
        return zbuf.getvalue()

# -*- coding=utf-8 -*-
################################################################################
#
# the Huskar framework
# @author dongliqiang@baidu.com
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
################################################################################

import finbull.log

# error ok
ERRNO_OK = 0
ERRMSG_OK = "ok"
# the framework errno
ERRNO_FRAMEWORK = 9999
ERRMSG_FRAMEWORK = "the FinBull framework error"

ERRNO_UNKNOWN = 9998
ERRMSG_UNKNOWN = "unknown error"

ERROR = {
    ERRNO_OK: ERRMSG_OK,
    ERRNO_FRAMEWORK: ERRMSG_FRAMEWORK,
    ERRNO_UNKNOWN: ERRMSG_UNKNOWN
}


class BaseError(Exception):
    """
    every Error should extend BaseError
    """

    def __init__(self, errno=ERRNO_FRAMEWORK, errmsg=None):
        """
        check error or errmsg
        """
        if errno in ERROR:
            self.errno = errno
            if errmsg is None:
                self.errmsg = ERROR[errno]
            else:
                self.errmsg = errmsg
        else:
            self.errno = ERRNO_UNKNOWN
            if errmsg is None:
                self.errmsg = ERROR[ERRNO_UNKNOWN]
            else:
                self.errmsg = errmsg

        finbull.log.warning({
            "finbull.error": "FinbullBaseError",
            "errno": self.errno,
            "errmsg": self.errmsg,
        })

        super(BaseError, self).__init__(errmsg)

# -*- coding=utf-8 -*-

import ast
import importlib
import inspect
import os
import sys
import traceback

# import tornado
# import tornado.concurrent
# import tornado.gen
# import tornado.httpserver
# import tornado.ioloop
# import tornado.web

import finbull.conf
import finbull.error


# private functions


def _get_app_path():
    """
    get the app path from traceback
    """
    t = traceback.extract_stack()
    for i, k in zip(t, t[1:]):
        # __file__ will return the .pyc in runtime
        # but the traceback only return .py
        # FIXED: run in optimizations mode
        # FIXED: run in symbolic links path
        if k[0] == os.path.abspath(__file__) or \
                k[0] + "c" == os.path.abspath(__file__) or \
                k[0] + "o" == os.path.abspath(__file__):
            return os.path.abspath(os.path.dirname(i[0]))


def _get_decorators(cls):
    """
    get the all decorators of the class
    :param cls:
    :return:
    """
    target = cls
    decorators = {}

    def visit(node):
        """
        NodeVisitor.visit_FunctionDef
        """
        decorators[node.name] = []
        for n in node.decorator_list:
            name = ""
            if isinstance(n, ast.Call):
                name = n.func.attr if isinstance(n.func, ast.Attribute) else n.func.id
            else:
                name = n.attr if isinstance(n, ast.Attribute) else n.id
            decorators[node.name].append(name)

    node_iter = ast.NodeVisitor()
    node_iter.visit_FunctionDef = visit
    node_iter.visit(ast.parse(inspect.getsource(target)))
    return decorators


def _check_decorators(cls_name, cls, func_name, decorator_names):
    """
    check the method decorated with the decorator.
    """
    all_decorators = _get_decorators(cls)
    # if the method is not defined in the class
    # we don't need to check the decorators
    if func_name not in all_decorators:
        return True

    exist = bool([d for d in all_decorators[func_name] if d in decorator_names])
    if exist is False:
        raise finbull.error.BaseError(
            errno=finbull.error.ERRNO_FRAMEWORK,
            errmsg="this module[%s] function[%s] must decorate with[%s]." % (
                cls_name, func_name, decorator_names)
        )
    return exist


def _load_all_classes(dirname, module_list, extends):
    """
    load all class into memory
    """
    if dirname is None or not os.path.isdir(dirname):
        raise finbull.error.BaseError(
            errno=finbull.error.ERRNO_FRAMEWORK,
            errmsg="load all class failed. dirname is None or error."
        )
    if module_list is None or len(module_list) < 1:
        raise finbull.error.BaseError(
            errno=finbull.error.ERRNO_FRAMEWORK,
            errmsg="load all class failed. module is None or error."
        )

    # you can not split all the module_list by "." and check the same name
    # because the dir maybe the same which is available
    # so it is ugly :(

    # `somemodule1.Class1` and `somemodule1.Class2` is available
    # cause it is the same module in the same path.
    # but `dir.module1` and `dir.dir2.module1` is unavailable
    # because the `dir` and `dir.dir2` should insert into `sys.path`
    # when you `import module1`
    # I don't know which `module1` should be imported.
    modules = [cls[:cls.rfind(".")] for cls in module_list]
    modules = sorted([".".join(reversed(m.split("."))) for m in modules])
    for i, m in enumerate(modules):
        if i == 0 or m.find(".") == -1 or modules[i - 1].find(".") == -1:
            continue
        if m == modules[i - 1]:
            continue
        # same module name
        if m[:m.find(".")] == modules[i - 1][:modules[i - 1].find(".")]:
            raise finbull.error.BaseError(
                errno=finbull.error.ERRNO_FRAMEWORK,
                errmsg="finbull do not support the module that has the same name[%s:%s]" % (
                    ".".join(reversed(m.split("."))),
                    ".".join(reversed(modules[i - 1].split(".")))
                )
            )

    # class name can not be the same
    # because I get all classes from `extend.__subclass__`
    # which is not include the path and has the class name only
    classes = [cls[cls.rfind("."):] for cls in module_list]
    same_classes = [x for x in classes if classes.count(x) > 1]
    if len(same_classes) > 0:
        raise finbull.error.BaseError(
            errno=finbull.error.ERRNO_FRAMEWORK,
            errmsg="finbull do not support the class that has the same name[%s]" % same_classes
        )

    # add top dir into sys.path
    sys.path.insert(0, dirname)
    try:
        for m in module_list:
            # if this module is submodule.
            # we should set the submodule's dir into sys.path
            # eg. the module is `somedir.somesubdir.somestrategy.Class`
            # so the submodule must have two `.` at least
            if m.count(".") >= 2:
                # first: include the `somedir.somesubdir` into the `sys.path`
                # m = somedir.somesubdir
                tmp_module = m[:m.rfind(".", 0, m.rfind("."))]
                # replace "." to "/"
                # tmp_path = dirname + "/a/b/c"
                tmp_path = dirname + "/" + tmp_module.replace(".", "/")
                # insert the path
                sys.path.insert(0, tmp_path)
                # second: import the module
                # module should be `somestrategy`
                cur_module = m[len(tmp_module) + 1:m.rfind(".")]
                importlib.import_module(cur_module)
                # third: remove the path
                sys.path.remove(tmp_path)
            else:
                # in the top dir
                importlib.import_module(m[:m.rfind(".")])

    except ImportError as e:
        raise finbull.error.BaseError(
            errno=finbull.error.ERRNO_FRAMEWORK,
            errmsg="import module failed: %s. module[%s]" % (e, m)
        )
    sys.path.remove(dirname)

    # check the classes exist and return
    all_classes = {}
    for cls in extends.__subclasses__():
        for m in module_list:
            cls_name = m[m.rfind(".") + 1:]
            if cls.__name__ == cls_name:
                all_classes[m] = cls
    return all_classes


"""
#######################
initialize variable
#######################s
"""

# # constant
# DIR_APP = _get_app_path()
# sys.path.insert(0, DIR_APP)
# DIR_BASE = os.path.dirname(DIR_APP)
# DIR_LOG = DIR_BASE + "/logs/"
# DIR_CONF = DIR_BASE + "/conf/"
# DIR_DATA = DIR_BASE + "/data/"
# DIR_APP_STRATEGY = DIR_APP + "/strategy/"
# DIR_APP_HANDLER = DIR_APP + "/handler/"
#
# # conf
# CONF_IDC = conf.Conf(infile=DIR_CONF + "idc.conf")
# CURRENT_IDC = CONF_IDC["idc"]
# CONF_APP = conf.Conf(infile=DIR_CONF + "app.conf", _idc=CURRENT_IDC)
# CONF_ERROR = conf.Conf(infile=DIR_CONF + "error.conf", _idc=CURRENT_IDC)
# """
# In handlers parameter section
# eg. `cuid = string(min=32, max=32)`
# ConfigObj should resolve "," to the list
# because this config file is not a configspec file.
# so "cuid" will be `[u"string(min=32", u"max=32)"]`
# that's why I change `list_values` to `False`
#
# so CONF_HANDLER dose NOT support a list value.
# but I think it will not be used:)
# """
# CONF_HANDLER = conf.Conf(infile=DIR_CONF + "handler.conf",
#                          _idc=CURRENT_IDC, list_values=False)
# CONF_FLOW = conf.Conf(infile=DIR_CONF + "flow.conf", _idc=CURRENT_IDC)
# CONF_SERVICE = conf.Conf(infile=DIR_CONF + "service.conf", _idc=CURRENT_IDC)
# CONF_STRATEGY = conf.Conf(infile=DIR_CONF + "strategy.conf", _idc=CURRENT_IDC)
# CONF_DATA = conf.Conf(infile=DIR_CONF + "data.conf", _idc=CURRENT_IDC)
#
# ALL_CONF = {
#     "idc": CONF_IDC,
#     "CURRENT_IDC": CURRENT_IDC,
#     "app": CONF_APP,
#     "error": CONF_ERROR,
#     "handler": CONF_HANDLER,
#     "flow": CONF_FLOW,
#     "service": CONF_SERVICE,
#     "strategy": CONF_STRATEGY,
#     "data": CONF_DATA,
# }
#
# # logger init
# finbull.log.init(DIR_LOG, CONF_APP["common"]["app_name"], CONF_APP["common"]["debug"])
# finbull.log.notice("finbull.init", "load all conf successfully.")
#
#
# def run():
#     # get all strategy classes
#     all_strategy_classes = []
#     for key in CONF_FLOW["strategy_chain"]:
#         if CONF_FLOW["strategy_chain"][key] is not None \
#                 and len(CONF_FLOW["strategy_chain"][key]) > 0:
#             all_strategy_classes.extend(CONF_FLOW["strategy_chain"][key])
#
#     if len(all_strategy_classes) > 0:
#         cls_strategy = _load_all_classes(DIR_APP_STRATEGY, set(
#             all_strategy_classes), finbull.strategy.BaseStrategy)
#
#         # check the decorators
#         # the `run` method of the strategy class
#         # MUST decorate with `finbull.thread` or `finbull.coroutine`
#         all_ = ["thread", "coroutine"]
#         for cls in cls_strategy:
#             _check_decorators(cls, cls_strategy[cls], "run", all_decorators)
#
#         finbull.log.notice({
#             "finbull.init": "load all strategy classes successfully.",
#             "cls_strategy": cls_strategy,
#         })
#     else:
#         finbull.log.notice("finbull.init", "there is no strategy class to be load.")
#
#     # get all handler classes
#     all_handler_classes = []
#     for key in CONF_HANDLER["handler"]:
#         if "handler" in CONF_HANDLER["handler"][key]["router"]:
#             if (CONF_HANDLER["handler"][key]["router"]["handler"] is not None and
#                     len(CONF_HANDLER["handler"][key]["router"]["handler"]) >= 1 and
#                     CONF_HANDLER["handler"][key]["router"]["handler"] != "BaseHandler"
#                     and CONF_HANDLER["handler"][key]["router"]["handler"]
#                     != "finbull.handler.BaseHandler"):
#                 all_handler_classes.append(CONF_HANDLER["handler"][key]["router"]["handler"])
#
#     if len(all_handler_classes) > 0:
#         cls_handler = _load_all_classes(DIR_APP_HANDLER, set(
#             all_handler_classes), finbull.handler.BaseHandler)
#
#         # check the decorators
#         # the `run_before` and `run_after` method of huandler class
#         # MUST decorate with `finbull.coroutine`
#         all_decorators = ["coroutine"]
#         for cls in cls_handler:
#             _check_decorators(cls, cls_handler[cls], "run_before", all_decorators)
#             _check_decorators(cls, cls_handler[cls], "run_after", all_decorators)
#
#         finbull.log.notice({
#             "finbull.init": "load all handler classes successfully.",
#             "cls_handler": cls_handler,
#         })
#     else:
#         finbull.log.notice("finbull.init", "there is no handler to be load.")
#
#     # load handler
#     handler = []
#     for key in CONF_HANDLER["handler"]:
#         # check parameter
#         # if you do not need check the parameter
#         # delete the parameter section in handler.conf
#         if "parameter" not in CONF_HANDLER["handler"][key]:
#             CONF_HANDLER["handler"][key]["parameter"] = None
#
#         if key not in CONF_FLOW["flow"]:
#             raise finbull.error.BaseError(
#                 errno=finbull.error.ERRNO_FRAMEWORK,
#                 errmsg="can not find the current handler in flow.conf. handler[%s]" % key
#             )
#
#         # BaseHandler by default
#         # if you do not hava any special requirement
#         # pu the "handler" section empty in router section of handler.conf
#         if "handler" not in CONF_HANDLER["handler"][key]["router"] or \
#                 CONF_HANDLER["handler"][key]["router"]["handler"] is None or \
#                 len(CONF_HANDLER["handler"][key]["router"]["handler"]) < 1 or \
#                 CONF_HANDLER["handler"][key]["router"]["handler"] == "BaseHandler" or \
#                 CONF_HANDLER["handler"][key]["router"]["handler"] == "finbull.handler.BaseHandler":
#
#             handler.append((CONF_HANDLER["handler"][key]["router"]["url"],
#                             finbull.handler.BaseHandler,
#                             dict(param_valid=CONF_HANDLER["handler"][key]["parameter"],
#                                  conf=ALL_CONF,
#                                  cls_strategy=cls_strategy,
#                                  handler_name=key)))
#         # handler by user
#         elif CONF_HANDLER["handler"][key]["router"]["handler"] in cls_handler:
#             handler.append((CONF_HANDLER["handler"][key]["router"]["url"],
#                             cls_handler[CONF_HANDLER["handler"][key]["router"]["handler"]],
#                             dict(param_valid=CONF_HANDLER["handler"][key]["parameter"],
#                                  conf=ALL_CONF,
#                                  cls_strategy=cls_strategy,
#                                  handler_name=key)))
#         else:
#             raise finbull.error.BaseError(
#                 errno=finbull.error.ERRNO_FRAMEWORK,
#                 errmsg="can not find the handler class[%s]" % CONF_HANDLER["handler"][key]
#             )
#
#     finbull.log.notice("finbull.init", "load handler successfully.")
#
#     # load error by custom
#     for key in CONF_ERROR["error"]:
#         setattr(finbull.error, key, CONF_ERROR["error"][key]["errno"])
#         setattr(finbull.error, key + "_MSG", CONF_ERROR["error"][key]["errmsg"])
#
#         finbull.error.ERROR[CONF_ERROR["error"][key]["errno"]] = \
#             CONF_ERROR["error"][key]["errmsg"]
#
#     finbull.log.notice("finbull.init", "load error successfully.")
#
#     # start the http server
#     app = tornado.web.Application(handler)
#     server = tornado.httpserver.HTTPServer(app)
#     server.bind(int(CONF_APP["httpserver"]["port"]))
#     server.start(int(CONF_APP["httpserver"]["process_num"]))
#
#     # in multiple processes
#     # start_processes must be called before ioloop instance.
#     loop = tornado.ioloop.IOLoop.instance()
#
#     # load data
#     finbull.data.DATA.load(CONF_DATA, DIR_DATA)
#     # start watching
#     # pyinotify monitor should use the tornado.ioloop
#     # so put it here.
#     finbull.data.DATA.watch()
#
#     # load service
#     finbull.service.SERVICE.load(CONF_SERVICE, CURRENT_IDC)
#
#     finbull.log.notice({
#         "finbull.init": "app started successfully.",
#         "app_name": CONF_APP["common"]["app_name"],
#         "port": CONF_APP["httpserver"]["port"],
#         "processes": CONF_APP["httpserver"]["process_num"],
#     })
#     loop.start()

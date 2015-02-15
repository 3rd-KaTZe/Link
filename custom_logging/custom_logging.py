# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Author:      Bob Daribouca
#
# Copyright:   (c) Bob Daribouca 2013
# Licence:     CC BY-NC-SA 3.0
#
#               Please refer to the "LICENSE" file distributed with the package,
#               or to http://creativecommons.org/licenses/by-nc-sa/3.0/
#
#-------------------------------------------------------------------------------
#!/usr/bin/env python
"""
This module provides an environement to make
module- and class-specific loggers
"""
import logging
from os.path import exists
from os import remove
DEBUG = logging.DEBUG
WARNING = logging.WARNING
INFO = logging.INFO
ERROR = logging.ERROR
WARN = WARNING
ERR = ERROR

def logged(f):
    """
    Decorator for the __init__ function of a class

    Adds a logger to an instance of that class, named:
    main.module.class.function
    """
    def wrapper(instance, *args, **kw):
        instance.logger = logging.getLogger(".".join(["main", instance.__class__.__name__]))
        return f(instance, *args, **kw)
    return wrapper


def mkLogger(moduleName, lvl=logging.DEBUG, logFile="link.log", custom_handler=None):
    """
    Creates a module-specific logger
    """
    if moduleName == "__main__":
        return __setupLogger("main", lvl, logFile, custom_handler)
    else:
        subLoggerName = ".".join(["main", moduleName])
    return logging.getLogger(subLoggerName)


def __setupLogger(name="main", lvl=logging.DEBUG, logFile="link.log", custom_handler=None):
    try:
        if exists(logFile):
            remove(logFile)
    except WindowsError:
        import sys
    logger = logging.getLogger(name)
    logger.setLevel(lvl)
    fh = logging.FileHandler(logFile)
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(lvl)
    logfileFormatter = logging.Formatter('%(asctime)s: %(levelname)s - %(name)s - %(funcName)s - %(message)s')
    consoleFormatter = logging.Formatter('%(levelname)s - %(name)s - %(funcName)s - %(message)s')
    fh.setFormatter(logfileFormatter)
    ch.setFormatter(consoleFormatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    if custom_handler:
        logger.addHandler(custom_handler)
    return logger

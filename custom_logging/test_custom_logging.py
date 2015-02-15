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

import unittest
import logging

try:
    import custom_logging
except ImportError:
    from . import custom_logging

class TestLoggingPackage(unittest.TestCase):

    def SetUp(self):
        pass

    def TearDown(self):
        pass

    def test_main_logger_init(self):
        logger = custom_logging.mkLogger("main")
        self.assertTrue(type(logger) == logging.Logger)


if __name__ == '__main__':
    unittest.main(verbosity=9)

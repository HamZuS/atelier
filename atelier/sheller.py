# -*- coding: UTF-8 -*-
# Copyright 2016 by Luc Saffre.
# License: BSD, see LICENSE for more details.

"""
Defines the :class:`Sheller` class.

"""

from __future__ import print_function
from builtins import str
# from builtins import input
from builtins import object
# Python 2 and 3:
from future.utils import python_2_unicode_compatible
import six
from six.moves import input

# from __future__ import unicode_literals
# causes problems on Windows where `subprocess.Popen` wants only plain strings

import os
import sys
import locale
import types
import datetime
import subprocess


class Sheller(object):

    def __init__(self, cwd=None):
        self.cwd = cwd

    def __call__(self, cmd, **kwargs):
        """Run the specified shell command `cmd` in a subprocess and print its
        output to stdout. This is designed for usage from within a doctest
        snippet.

        If `cmd` is a multiline string, semicolons are automatically
        inserted as line separators.

        One challenge is that we cannot simply use `subprocess.call`
        because `sys.stdout` is handled differently when running inside
        doctest.

        """
        cmd = [ln for ln in cmd.splitlines() if ln.strip()]
        cmd = ';'.join(cmd)

        if self.cwd:
            kwargs.update(cwd=self.cwd)

        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, shell=True, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        output = output.strip()
        print(output)
        # if(output):
        #     print(output.strip())
        # else:
        #     print("(exit status {})".format(retcode))

##############################################################################
#
# Copyright (c) 2019 Jens Vagelpohl and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
import unittest


SERVER = {}


def fake_run(app, host, **kw):
    global SERVER
    SERVER.clear()

    SERVER['app'] = app
    SERVER['host'] = host
    SERVER.update(kw)


class BjoernInitializationTests(unittest.TestCase):

    def test_initialization(self):
        # Install fake server class first
        from dataflake.wsgi import bjoern
        old_impl = bjoern.run
        bjoern.run = fake_run

        from dataflake.wsgi.bjoern import serve_paste

        global SERVER

        # The defaults
        serve_paste(None, None)
        self.assertEqual(SERVER['host'], '')
        self.assertEqual(SERVER['port'], False)
        self.assertEqual(SERVER['reuse_port'], False)

        # Host and port set
        serve_paste(None, None, host='localhost', port='8888', reuse_port='On')
        self.assertEqual(SERVER['host'], 'localhost')
        self.assertEqual(SERVER['port'], 8888)
        self.assertEqual(SERVER['reuse_port'], True)

        # Listen without host
        serve_paste(None, None, listen='8898')
        self.assertEqual(SERVER['host'], '')
        self.assertEqual(SERVER['port'], 8898)

        # Listen with host
        serve_paste(None, None, listen='127.0.0.2:8999')
        self.assertEqual(SERVER['host'], '127.0.0.2')
        self.assertEqual(SERVER['port'], 8999)

        # Clean up fake server class
        bjoern.run = old_impl

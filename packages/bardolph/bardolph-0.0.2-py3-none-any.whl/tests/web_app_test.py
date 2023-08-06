#!/usr/bin/env python

import unittest

from web.web_app import WebApp

class WebAppTest(unittest.TestCase):
    def test_get_title(self):
        app = WebApp()
        script = { 'path': 'test-get_title' } 
        self.assertEqual(app.get_title(script), 'Test Get Title')
        script = { 'file_name': 'test-get_title.ls' }
        self.assertEqual(app.get_title(script), 'Test Get Title')
        script = { 'file_name': 'test-get_title' }
        self.assertEqual(app.get_title(script), 'Test Get Title')
        
    def test_get_path(self):
        app = WebApp()
        script = { 'file_name': 'test.ls' } 
        self.assertEqual(app.get_path(script), 'test')
        script = { 'file_name': 'test.ls', 'path': 'test-path'}
        self.assertEqual(app.get_path(script), 'test-path')


if __name__ == '__main__':
    unittest.main()

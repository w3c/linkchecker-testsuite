#!/usr/bin/env python
# encoding: utf-8
"""
W3CLikCheckerClient.py
Simple client lib to interact with the W3C Link Checker

Created by olivier Thereaux on 2008-01-22.
Copyright (c) 2008 W3C. Licensed under the W3C Software License
http://www.w3.org/Consortium/Legal/copyright-software
"""

import sys
import os
import re
import unittest
from W3CLinkCheckerClient import W3CLinkCheckerClient

class LinkTestCase(unittest.TestCase):
    """Atomic Test Case for the link checker suite"""
    def __init__(self, title=None, description=None, docURI=None, runOptions=None, expectResults=None, checker=None):
        if title:
            self.title = title
        else:
            self.title = u''
        if docURI:
            self.docURI = docURI
        else: 
            self.docURI = ""
        if description:
            self.description = description
        else:
            self.description = u""
        if isinstance(runOptions, dict):
            self.runOptions = runOptions
        else:
            self.runOptions = dict()
        if isinstance(expectResults, dict):
            self.expectResults = expectResults
        else:
            self.expectResults = dict()
        if checker != None:
            self.checker = checker
        else:
            self.checker = W3CLinkCheckerClient()
        self._testMethodName= "run_testcase"

    def shortDescription(self):
        return self.title

    def run_testcase(self):
        """run a link checker test case"""         
        self.assertEqual(self.checker.parse_checklink(self.checker.call_checklink(self.docURI)), self.expectResults)

class LinkTestCollection():
    """Collection of Link Checker Test Cases"""
    def __init__(self, title=None, description=None, casefiles=None, cases=None):
        if title != None:
            self.title = title
        else:
            self.title = u""
        if description != None:
            self.description = description
        else:
            self.description = u""
        if (isinstance(casefiles, list)):
            self.casefiles = casefiles
        else:
            self.casefiles = list()
        if (isinstance(cases, list)):
            self.cases = cases
        else:
            self.cases = list()

class LinkTestCase_UT(unittest.TestCase):
    """Sanity Check for TestCase and TestCollection classes"""
    def test_1_init_default(self):
        """Test initialization of a default LinkTestCase Object"""
        default_tc = LinkTestCase()
        self.assertEqual(
            [default_tc.title, default_tc.description, default_tc.docURI, default_tc.runOptions, default_tc.expectResults],
            [u'', u'', '', dict(), dict()]
        )
        

if __name__ == '__main__':
    unittest.main()
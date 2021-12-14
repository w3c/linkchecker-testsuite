#!/usr/bin/env python
# encoding: utf-8
"""
W3CLikCheckerClient.py
Simple client lib to interact with the W3C Link Checker

Created by olivier Thereaux on 2008-01-22.
Copyright (c) 2008 W3C. Licensed under the W3C Software License
http://www.w3.org/Consortium/Legal/copyright-software
"""

import re
import unittest
import urllib.request, urllib.parse, urllib.error
import html5lib
import xml.etree.ElementTree as etree

class W3CLinkCheckerClient():
    """Fetch and parse results from W3C Link Checker CLI"""
    def __init__(self, checklink_path):
        self.checklink_path = checklink_path

    def call_checklink(self, TC_uri, TC_options=None):
        """Make a request to the link checker and store its response"""
        import subprocess
        res = subprocess.run(['/usr/bin/env', 'perl', '-T', self.checklink_path, "-H", "--follow-file-links", TC_uri],  capture_output=True)
        if res.stderr:
            raise Exception("checklink generated error:" + res.stderr.decode("utf-8"))
        return res.stdout.decode("utf-8")

    def parse_checklink(self, response):
        """Parse a W3C Link Checker response (HTML-scraping. baååååd.)"""
        tb = html5lib.getTreeBuilder("etree", implementation=etree)
        p = html5lib.HTMLParser(tb)
        try:
            tree = p.parse(response)
        except SyntaxError as v:
            raise v
        #reports = tree.find(".//dl[@class=’report’]")
        # won't be available before ET v1.3
        reports = dict()
        for dl_elt in tree.findall(".//{http://www.w3.org/1999/xhtml}dl"):
            # don't forget to look for elements in the xhtml namespace
            if "class" in dl_elt.attrib:
                if dl_elt.attrib["class"] == 'report':
                    for dt_elt in dl_elt.findall("./{http://www.w3.org/1999/xhtml}dt"):
                        message_class = None
                        if "id" in dt_elt.attrib:
                            message_class = re.sub(r'.*\_', '', dt_elt.attrib["id"])
                            message_uri = dt_elt.find("./{http://www.w3.org/1999/xhtml}a").attrib["href"]
                            if message_class in reports:
                                reports[message_class].append(message_uri)
                            else:
                                reports[message_class] = (message_uri)
        return reports

class OnlineW3CLinkCheckerClient(W3CLinkCheckerClient):
    """Fetch and parse results from online W3C Link Checker"""
    def __init__(self, checklink_cgi):
        self.checklink_cgi= checklink_cgi



    def call_checklink(self, TC_uri, TC_options=None):
        """Make a request to the link checker and store its response"""
        data = urllib.parse.quote(TC_uri, "")
        try:
            response = urllib.request.urlopen(self.checklink_cgi+"?uri="+data)
            return response
        except (urllib.error.HTTPError, urllib.error.URLError):
            return None


class W3CLinkCheckerClient_UT(unittest.TestCase):
    """Unit testing for sanity of W3CLinkCheckerClient code"""
    def setUp(self):
        pass


    def test_4_elementtree(self):
        """Check whether ElementTree parses basic XML and XPath support is high enough"""
        tb = html5lib.getTreeBuilder("etree", implementation=etree)
        p = html5lib.HTMLParser(tb)
        tree = p.parse('<foo />')
        try:
            tree.find(".//dl")
        except SyntaxError:
            assert 0, "could not compile xpath for all dl"

    def test_5_parse_checklink(self):
        """Parse a Controlled link checker response"""
        import os
        try:
            default_wlc = W3CLinkCheckerClient(os.environ['CHECKLINK_PATH'])
        except:
            import sys
            sys.stderr.write("Set CHECKLINK_PATH environment variable")
            sys.exit(2)
        wlc_response = default_wlc.call_checklink("http://checklink.test:9999/link-testsuite/base-2.html")
        wlc_reports = default_wlc.parse_checklink(wlc_response)
        self.assertTrue(isinstance(wlc_reports, dict), "parsing result should be a dict")
        self.assertEqual( len(list(wlc_reports.keys())), 1, "for this case, there should be one key-value pair in the parse dict")
        self.assertEqual( list(wlc_reports.keys())[0], '404', "for this case, there should be one 404 in the parse dict")

if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python
# encoding: utf-8
"""
link-testsuite/harness/run.py
Run or Generate test suite for link checkers

Created by olivier Thereaux on 2008-01-23.
Copyright (c) 2008 W3C. Licensed under the W3C Software License
http://www.w3.org/Consortium/Legal/copyright-software
"""

import os
import sys
import glob
import getopt
import unittest
import xml.etree.cElementTree as ET

basedir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(basedir, "lib"))
from W3CLinkCheckerClient import W3CLinkCheckerClient, W3CLinkCheckerClient_UT
from LinkTestCase import LinkTestCase, LinkTestCase_UT, LinkTestCollection
from Documentation import Documentation
help_message = '''

Run or Generate test suite for link checkers

Usage: linktest.py [options] [run|sanity|doc]
    Options: 
        -h, --help: this manual you are reading
        -v, --verbose: verbose output
        -q, --quiet: suppress all output except errors
        --checker_uri: use a specific link checker instance
          e.g http://validator.w3.org/checklink

    Modes:
        run: run the link checker test suite 
        sanity: check that this code is still working 
            useful after using test cases or modifying code
        doc: generate an HTML index of the test cases
'''



class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

class TestRun(unittest.TestCase):
    def test_1_1_readTestCase(self):
        """Opening and parsing a Test Case file (basic)"""
        basedir = getBaseDir()
        test_file = os.path.join(basedir, 'sample', 'sample.test')
        sample_test = readTestCase(test_file)
        self.assert_(isinstance(sample_test, LinkTestCase))

      
    def test_1_2_readTestCase(self):
        """Opening and parsing a Test Case file (values)"""
        basedir = getBaseDir()
        test_file = os.path.join(basedir, 'sample', 'sample.test')
        sample_test = readTestCase(test_file)
        self.assertEqual(
          (sample_test.title,
          sample_test.description, 
          sample_test.docURI, 
          sample_test.runOptions, 
          sample_test.expectResults),
         (u"Sample Test case for a 404", 
         u'''The document links to a 404 not found resource.\n        The checker should report the broken link''',
         "http://checklink.test/link-testsuite/http-404.html", 
         {}, 
         {"404": "http://checklink.test/link-testsuite/http?code=404"})
        )
    
    def test_1_3_readTestCase(self):
        """Ill-formed test case files should throw an exception"""
        basedir = getBaseDir()
        test_file = os.path.join(basedir, 'sample', 'sampleillformed.test')
        self.assertRaises(SyntaxError, readTestCase, test_file)
    
    def test_2_1_readCollectionMeta(self):
        """Opening and parsing a Test Collection metadata file (basic)"""
        basedir = getBaseDir()
        collection_file = os.path.join(basedir, 'sample', 'sample.collection')
        sample_collection = readCollectionMeta(collection_file)
        self.assert_(isinstance(sample_collection, LinkTestCollection))    
    
    def test_2_2_readCollectionMeta(self):
        """Opening and parsing a Test Collection metadata file (values)"""
        basedir = getBaseDir()
        collection_file = os.path.join(basedir, 'sample', 'sample.collection')
        sample_collection = readCollectionMeta(collection_file)
        self.assertEqual(
          (sample_collection.title, sample_collection.description, sample_collection.casefiles),
          (u"test", u"Sample Collection with one test", ["sample.test"])
        )
    
    def test_3_buildTestCollection(self):
        """Test building a Test Collection"""
        basedir = getBaseDir()
        collection_file = os.path.join(basedir, 'sample', 'sample.collection')
        sample_collection = readCollectionMeta(collection_file)
        for testcase_file in sample_collection.casefiles:
            test_file = os.path.join(basedir, 'sample', testcase_file)
            sample_test = readTestCase(test_file)
            self.assertEqual(
              (sample_test.title,
               sample_test.description,
              sample_test.docURI, 
              sample_test.runOptions, 
              sample_test.expectResults),
              (u"Sample Test case for a 404", 
              u'''The document links to a 404 not found resource.\n        The checker should report the broken link''',
              "http://checklink.test/link-testsuite/http-404.html", 
              {}, 
              {"404": "http://checklink.test/link-testsuite/http?code=404"})
             )
    
    def test_4_buildTestSuite(self):
        """Test building the whole Link Checker Test Suite"""
        suite = buildTestSuite()
        pass

def main(argv=None):
    verbose=1
    checker_uri = None
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "ho:vq", ["help", "output=", "verbose", "quiet", "checker_uri="])
            for (opt, value) in opts:
                if opt == "h" or opt == "--help":
                    raise Usage(msg)
        except getopt.error, msg:
            raise Usage(msg)
    
        # option processing
        for option, value in opts:
            if option in ("-v", "--verbose"):
                verbose = 2
            if option in ("-q", "--quiet"):
                verbose = 0
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-o", "--output"):
                output = value
            if option == "--checker_uri":
                checker_uri = value

        if len(args) == 0:
            raise Usage(help_message)
    
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2

        
    if args[0] == "run":
        checker = None
        if checker_uri:
            checker = W3CLinkCheckerClient(checker_uri)
        suite = buildTestSuite(checker)
        unittest.TextTestRunner(verbosity=verbose).run(suite)
    elif args[0] == "sanity":
        suite1 = unittest.TestLoader().loadTestsFromTestCase(W3CLinkCheckerClient_UT)
        suite2 = unittest.TestLoader().loadTestsFromTestCase(LinkTestCase_UT)
        suite3 = unittest.TestLoader().loadTestsFromTestCase(TestRun)
        suite = unittest.TestSuite([suite1, suite2, suite3])
        unittest.TextTestRunner(verbosity=verbose).run(suite)
        
    elif args[0] == "doc":
        generateIndex()

def getBaseDir():
    basedir = os.path.dirname(os.path.abspath(__file__))
    return basedir

def readTestCase(test_file, checker=None):
    test_file_handle = open(test_file, 'r')
    try:
        tree = ET.parse(test_file_handle)
    except SyntaxError, v:
        raise v
    title = tree.findtext("title")
    if title:
        title = title.decode("utf-8")
    else:
        title = None
    descr = tree.findtext("description")
    if descr:
        descr = descr.decode("utf-8")
    else:
        descr = None
    doc_elt = tree.find(".//doc")
    if doc_elt.attrib.has_key("href"):
        test_uri = doc_elt.attrib["href"]
    else:
        test_uri = None
    options_elt = tree.find(".//options")
    ## TODO
    expect_elt = tree.find(".//expect")
    expected = dict()
    if expect_elt.getchildren():
        for child in expect_elt.findall("report"):
            if child.attrib.has_key("href") and child.attrib.has_key("code"):
                if expected.has_key(child.tag):
                    expected[child.attrib["code"]].append(child.attrib["href"])
                else:
                    expected[child.attrib["code"]] = (child.attrib["href"])
                
    case = LinkTestCase(title=title, description=descr, docURI=test_uri, runOptions=None, expectResults=expected, checker=checker)
    return case

def readTestCollection(collection_path):
    basedir = getBaseDir()
    
    for metafile in glob.glob(os.path.join(collection_path, '*.collection')):
        collection = readCollectionMeta(metafile)

def readCollectionMeta(collection_file, checker=None):
    collection_file_handle = open(collection_file, 'r')
    collection_path = os.path.dirname(os.path.abspath(collection_file))
    try:
        tree = ET.parse(collection_file_handle)
    except SyntaxError, v:
        raise v
    title = tree.findtext("title")
    if title:
        title = title.decode("utf-8")
    else:
        title = u""
    description = tree.findtext("description")
    if description:
        description = description.decode("utf-8")
    else:
        description = u""
    tests = list()
    for test in tree.findall("testcase"):
        if test.attrib.has_key("src"):
            tests.append(test.attrib["src"])
        else:
            tests.append(test.tag)
    collection = LinkTestCollection(title=title, description=description, casefiles=tests)
    for testfile in collection.casefiles:
        case = readTestCase(os.path.join(collection_path, testfile), checker=checker)
        collection.cases.append(case)
    return collection

def generateIndex():
    index = Documentation('index')
    for testcollection_file in (glob.glob(os.path.join(basedir, 'testcases', '**', '*.collection'))):
        colldir = os.path.dirname(os.path.abspath(testcollection_file))
        colldir = os.path.split(colldir)[-1]        
        testcollection = readCollectionMeta(testcollection_file)
        index.addCollection(testcollection)
    print index.generate(template_path=os.path.join(basedir, "templates")).encode('utf-8')

def buildTestSuite(checker=None):
    suite = unittest.TestSuite()
    basedir = getBaseDir()
    for testcollection_file in (glob.glob(os.path.join(basedir, 'testcases', '**', '*.collection'))):
        colldir = os.path.dirname(os.path.abspath(testcollection_file))
        colldir = os.path.split(colldir)[-1]
        
        testcollection = readCollectionMeta(testcollection_file, checker=checker)
        for case in testcollection.cases:
            suite.addTest(case)
    return suite


if __name__ == "__main__":
    sys.exit(main())

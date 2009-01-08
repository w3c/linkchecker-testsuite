#!/usr/bin/env python
# encoding: utf-8
"""
Documentation.py
Generate Link Test Suite index and documentation

Created by olivier Thereaux on 2008-01-30.
Copyright (c) 2008 W3C. Licensed under the W3C Software License
http://www.w3.org/Consortium/Legal/copyright-software
"""

import sys
import os
import unittest
import LinkTestCase
import datetime

class Documentation:
    def __init__(self, type=None):
        ok_types = ['test', 'index']
        if type in ok_types:
            self.type = type
        else:
            self.type = 'index'
        self.test_collections = list()
    def addCollection(self, test_collection):
        if isinstance(test_collection, LinkTestCase.LinkTestCollection) == 0:
            raise TypeError("not a proper test collection") 
        else:
            self.test_collections.append(test_collection)
    
    def generate(self, template_path=None):
        """pass through template engine"""
        import jinja2,datetime
        if template_path == None:
            template_path= os.path.abspath('..')
            template_path=os.path.join(template_path, "templates")    
        template_engine = jinja2.Environment(loader=jinja2.FileSystemLoader(template_path))
        template = template_engine.get_template(os.path.join(self.type+'.html'))
        return template.render(collections=self.test_collections,
        year=str(datetime.date.today().year))

class DocumentationTests(unittest.TestCase):
    def test_has_jinja2(self):
        try:
            import jinja2
        except ImportError:
            self.fail("you need to install the jinja2 templating system -- http://jinja.pocoo.org/2/")

    def test_init(self):
        """initialize a Documentation Generator"""
        generator = Documentation()
        self.assertEquals(generator.type, 'index')
    
    def test_init_default_fallback(self):
        """initialize a Documentation Generator with a bogus type"""
        generator = Documentation(type="grut")
        self.assertEquals(generator.type, 'index')

    def test_addCollection(self):
        """add test collection"""
        generator = Documentation()
        test_col = LinkTestCase.LinkTestCollection()
        generator.addCollection(test_col)
        self.assertEquals(len(generator.test_collections), 1)
    
    def test_boguscollection(self):
        """add bogus test collection and raise error"""
        generator = Documentation()
        test_col = 5 
        self.assertRaises(TypeError, Documentation.addCollection, generator, test_col)
    
    def test_generate_test(self):
        """generate collections index without any collection"""
        generator = Documentation('test')
        self.assertEqual(generator.generate(), str(datetime.date.today().year))


if __name__ == '__main__':
    unittest.main()
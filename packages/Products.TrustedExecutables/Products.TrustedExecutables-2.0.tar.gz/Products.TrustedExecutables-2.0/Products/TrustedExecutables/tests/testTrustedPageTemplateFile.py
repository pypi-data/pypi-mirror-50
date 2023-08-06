# Copyright (C) 2004-2019 by Dr. Dieter Maurer, Eichendorffstr. 23, D-66386 St. Ingbert, Germany
# see "LICENSE.txt" for details
#       $Id: testTrustedPageTemplateFile.py,v 1.3 2019/08/16 07:02:44 dieter Exp $

from .TestBase import TestCase

from Products.TrustedExecutables.TrustedPageTemplateFile import \
     TrustedPageTemplateFile

class TestTrustedPageTemplateFile(TestCase):
  def testNoUnauthorized(self):
    f = self.folder
    fi = TrustedPageTemplateFile('Files/pt.xpt', globals()).__of__(f)
    fi() # we succeed unless we get an exception

  def testCallPy(self):
    # test that calling a python script from a trusted page template succeeds
    # (this broke in version 1.0.0)
    fi = self.folder.Files
    self.assertEqual(fi.pt_call_py().rstrip(), 'test')

# Copyright (C) 2004-2019 by Dr. Dieter Maurer, Eichendorffstr. 23, D-66386 St. Ingbert, Germany
# see "LICENSE.txt" for details
#       $Id: testTrustedFSObjects.py,v 1.2 2019/08/16 07:02:44 dieter Exp $
from .TestBase import TestCase, getSuite

class TestTrustedFSObjects(TestCase):
  def testPageTemplate(self):
    fi = self.folder.Files
    fi.pt() # we succeed unless we get an exception

  def testPythonScript(self):
    fi = self.folder.Files
    self.assertEqual(fi.py().rstrip(), 'test')

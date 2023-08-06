# Copyright (C) 2004 by Dr. Dieter Maurer, Eichendorffstr. 23, D-66386 St. Ingbert, Germany
# see "LICENSE.txt" for details
#       $Id: TestBase.py,v 1.2 2019/08/16 07:02:44 dieter Exp $
'''Test base class.

The 'TrustedExecutables' tests use 'ZopeTestCase'.
You must install this package separately (under 'lib/python/Testing').
You can get 'ZopeTestCase' from Zope.org.
'''

from os.path import join
from sys import modules
from unittest import TestSuite, makeSuite

from App.version_txt import getZopeVersion
from Testing.ZopeTestCase import ZopeTestCase, installProduct
from Testing.ZopeTestCase.layer import ZopeLite
from zope import component
from zope.component import globalregistry, _api
from zope.component.globalregistry import \
     globalSiteManager, BaseGlobalComponents
from zope.component.hooks import getSite, setSite
from zope.configuration.xmlconfig import file as load_config

from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore.utils import getContainingPackage

prefix = getContainingPackage(__name__)

installProduct('CMFCore', 1)
installProduct('Five', 1)
registerDirectory('Files', globals())

class Layer(ZopeLite):
  context = None

  @classmethod
  def setUp(cls):
    cls.reg = globalSiteManager
    # set up new component registry
    globalregistry.base = globalregistry.globalSiteManager = BaseGlobalComponents("base")
    # `_api` caches `base` -- invalidate
    _api.base = None
    # in a Plone environment `setSite` has been called and cached `base`
    #   reset
    cls.site = getSite()
    setSite(None)
    if getZopeVersion()[0] == 2:
      # initialize
      cls.context = load_config("meta.zcml", component, cls.context)
    cls.context = load_config("configure.zcml", modules[prefix], cls.context)

  @classmethod
  def tearDown(cls):
    # restore former registry
    globalregistry.base = globalregistry.globalSiteManager = cls.reg
    # `_api` caches `base` -- invalidate
    _api.base = None
    setSite(cls.site)
    cls.context = None
    

class TestCase(ZopeTestCase):
  layer = Layer

  def afterSetUp(self):
    folder = self.folder
    folder.manage_addProduct['CMFCore'].manage_addDirectoryView(
      prefix + ':Files', 'Files'
      )


def getSuite(*testClasses, **kw):
  prefix= kw.get('prefix','test')
  return TestSuite([makeSuite(cl,prefix) for cl in testClasses])
  

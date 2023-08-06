# Copyright (C) 2004-2019 by Dr. Dieter Maurer, Illtalstr. 25, D-66571 Bubach, Germany
# see "LICENSE.txt" for details
#       $Id: TrustedFSPageTemplate.py,v 1.3 2019/08/16 07:02:44 dieter Exp $
'''FSPageTemplate unrestricted by Zopes security'''

import sys

from Products.CMFCore.FSPageTemplate import \
     FSPageTemplate, \
     PageTemplate, \
     registerFileExtension

from dm.reuse import rebindFunction
from .Utils import _UnCustomizable
from .TrustedExpression import getEngine, ModuleImporter

class TrustedFSPageTemplate(_UnCustomizable, FSPageTemplate):
  
  meta_type = 'Trusted Filesystem Page Template'

  pt_getEngine = staticmethod(getEngine)

  pt_getContext = rebindFunction(FSPageTemplate.pt_getContext,
                                 SecureModuleImporter=ModuleImporter,
                                 )


registerFileExtension('xpt', TrustedFSPageTemplate)

# Copyright (C) 2004-2019 by Dr. Dieter Maurer, Illtalstr. 25, D-66571 Bubach, Germany
# see "LICENSE.txt" for details
#       $Id: TrustedPageTemplateFile.py,v 1.2 2019/08/16 07:02:44 dieter Exp $
'''A 'PageTemplateFile' without security restrictions.'''

from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from dm.reuse import rebindFunction
from .TrustedExpression import getEngine, ModuleImporter


class TrustedPageTemplateFile(PageTemplateFile):
  pt_getEngine = rebindFunction(PageTemplateFile.pt_getEngine,
                                  getEngine = getEngine
                                  )

  pt_getContext = rebindFunction(PageTemplateFile.pt_getContext,
                                 SecureModuleImporter=ModuleImporter,
                                 )


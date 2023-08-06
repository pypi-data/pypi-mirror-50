# Copyright (C) 2019 by Dr. Dieter Maurer, Illtalstr. 25, D-66571 Bubach, Germany
# see "LICENSE.txt" for details
#       $Id: TrustedPythonScriptMixin.py,v 1.2 2019/08/16 07:02:44 dieter Exp $
'''Auxiliary mixin class to implement trusted PythonScripts.'''
from App.version_txt import getZopeVersion

if getZopeVersion()[0] >= 4: from .pymixin_4 import TrustedPythonScriptMixin
else: from .pymixin_2  import TrustedPythonScriptMixin

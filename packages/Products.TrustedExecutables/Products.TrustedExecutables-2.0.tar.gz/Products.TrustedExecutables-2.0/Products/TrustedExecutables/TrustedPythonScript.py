# Copyright (C) 2004-2019 by Dr. Dieter Maurer, Illtalstr. 25, D-66571 Bubach, Germany
# see "LICENSE.txt" for details
#       $Id: TrustedPythonScript.py,v 1.2 2019/08/16 07:02:44 dieter Exp $
'''Python Script unrestricted by Zopes security.

CAUTION: Almost surely, you do not want to make this available.
'''

from Products.PythonScripts.PythonScript import PythonScript

from .TrustedPythonScriptMixin import TrustedPythonScriptMixin

class TrustedPythonScript(TrustedPythonScriptMixin, PythonScript):
  '''Python Script unrestriced by Zopes security.'''
  meta_type = 'Trusted Python Script'

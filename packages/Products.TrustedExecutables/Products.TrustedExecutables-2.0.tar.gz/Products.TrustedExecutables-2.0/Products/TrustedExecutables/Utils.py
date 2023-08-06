# Copyright (C) 2004-2019 by Dr. Dieter Maurer, Illtalstr. 25, D-66571 Bubach, Germany
# see "LICENSE.txt" for details
#       $Id: Utils.py,v 1.2 2019/08/16 07:02:44 dieter Exp $
'''Utilities'''

from ExtensionClass import Base

class _UnCustomizable(Base):
  '''mixin class to prevent customization.'''
  def manage_doCustomize(self):
    "do not allow customization"
    raise TypeError('This object does not support customization')

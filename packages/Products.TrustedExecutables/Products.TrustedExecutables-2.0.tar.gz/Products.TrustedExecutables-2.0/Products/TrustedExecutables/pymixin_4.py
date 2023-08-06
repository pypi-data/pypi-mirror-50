# Copyright (C) 2019 by Dr. Dieter Maurer, Illtalstr. 25, D-66571 Bubach, Germany
# see "LICENSE.txt" for details
#       $Id: pymixin_4.py,v 1.1 2019/08/16 07:02:44 dieter Exp $
'''Auxiliary mixin class to implement trusted PythonScripts.'''
try: import __builtin__ # Python 2
except ImportError: import builtins as __builtin__ # Python 3
from operator import getitem

from AccessControl.ZopeGuards import _metaclass, protected_inplacevar
from ExtensionClass import Base
from RestrictedPython import PrintCollector
from RestrictedPython.Guards import \
     guarded_iter_unpack_sequence, guarded_unpack_sequence
from RestrictedPython.compile import \
     compile_restricted_function, RestrictingNodeTransformer

from Products.PythonScripts.PythonScript import PythonScript

from dm.reuse import rebindFunction


_Globals = dict(
  __builtins__=__builtin__.__dict__,
  __metaclass__=_metaclass,
  _apply_=lambda f, *args, **kw: f(*args, **kw),
  _getitem_=getitem,
  _getiter_=iter,
  _iter_unpack_sequence_=guarded_iter_unpack_sequence,
  _unpack_sequence_=guarded_unpack_sequence,
   _print_=PrintCollector,
  _write_=lambda ob:ob,
  _inplace_var_=rebindFunction(protected_inplacevar,
                               isinstance=lambda *args: True),
  )
  
class _UnrestrictingNodeTransformer(RestrictingNodeTransformer):
  def error(*args, **kw): pass # everything is allowed

  def generic_visit(self, node):
    return self.node_contents_visit(node) # transform children


class TrustedPythonScriptMixin(Base):
  _newfun = rebindFunction(PythonScript._newfun,
                           get_safe_globals = _Globals.copy,
                           guarded_getattr = getattr,
                           )
  _compile = rebindFunction(
    PythonScript._compile,
    compile_restricted_function=rebindFunction(
      compile_restricted_function,
      argRebindDir=dict(policy=_UnrestrictingNodeTransformer)
      )
                            )

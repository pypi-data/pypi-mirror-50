TrustedExecutables is a set of executable objects unrestricted
by Zope[2]'s security.
Currently, it contains 'TrustedPageTemplateFile',
'TrustedFSPageTemplate' and 'TrustedFSPythonScript'.
'TrustedFSPageTemplate' and 'TrustedFSPythonScript' are registered
with the filename extensions 'xpt' and 'xpy', respectively.

As Zope's security checks are expensive, avoiding them can
drastically speed things up.

On the other hand, these objects must make their own security
checks at places where access control is required.

Use with extreme care!


ATTENTION: It is not unlikely that this product breaks between
Zope releases, as it uses undocumented implementation artefacts.
It is probably not very difficult to fix things again but
you will need programming skills to do so.


History

  2.0

    Python 3/Zope 4 compatibility

    Note: newer TALES expression types (``defer``, ``lazy``,
    ``provider``) might still perform authorization checks
    (and thus do not yet trust).

  1.0

    for Zope 2.11+

from os.path import abspath, dirname, join
try:
  # try to use setuptools
  from setuptools import setup
  setupArgs = dict(
      install_requires=[
      'dm.reuse',
      "setuptools", # to make `buildout` happy
      # depends on `Zope2/Zope [4]`
      # the `*FS*` executables depend on `Products.CMFCore`
      ],
      include_package_data=True,
      namespace_packages=['Products'],
      zip_safe=False, # to let the tests work
      )
except ImportError:
  # use distutils
  from distutils import setup
  setupArgs = dict(
    )

cd = abspath(dirname(__file__))
pd = join(cd, 'Products', 'TrustedExecutables')

def pread(filename, base=pd): return open(join(base, filename)).read().rstrip()

setup(name='Products.TrustedExecutables',
      version=pread('VERSION.txt').split('\n')[0],
      description='Trusted Zope 2 executables (scripts, templates) -- unrestricted by Zope 2 security. For Zope 2.13 and above',
      long_description=pread('README.txt'),
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Framework :: Zope2',
        'Framework :: Zope',
        'Framework :: Zope :: 4',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
        ],
      author='Dieter Maurer',
      author_email='dieter@handshake.de',
      url='http://www.dieter.handshake.de/pyprojects/zope',
      packages=['Products', 'Products.TrustedExecutables', 'Products.TrustedExecutables.tests'],
      keywords='Zope 2, trusted, executables, unrestricted, security ',
      license='BSD (see "Products/TrustedExecutables/LICENSE.txt", for details)',
      **setupArgs
      )




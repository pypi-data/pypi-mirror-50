from distutils.core import setup
setup(
name='nai',
version='3.1',
author='Nasir Ali',
author_email='nasiralis1731@gmail.com',
author_url='https://facebook.com/nasir.xo',
packages=['nai'],
scripts=[
'bin/phone',
'bin/roll',
'bin/ndb',
'bin/quote',
'bin/joke',
'bin/darknex',
'bin/mailspam',
'bin/mailspoof',
],
install_requires=[
'bs4',
'requests',
'ak47',
'nfd',
'flb'
, ],
)

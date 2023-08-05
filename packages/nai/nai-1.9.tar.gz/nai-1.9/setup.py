from distutils.core import setup
setup(
name='nai',
version='1.9',
author='Nasir Ali',
author_email='nasiralis1731@gmail.com',
author_url='https://facebook.com/nasir.xo',
packages=['nai'],
scripts=['bin/phone','bin/roll'],
install_requires=['bs4','requests', ],
)

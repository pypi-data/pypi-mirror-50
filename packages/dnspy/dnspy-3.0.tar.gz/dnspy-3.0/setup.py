
from distutils.core import setup

setup(name='dnspy',
      version='3.0',
      description='Library for fully qualified domain name (FQDN) manipulation',
      author='Sandeep Yadav',
      url='https://github.com/sandeepvaday/dnspy',
      packages=['dnspy'],
      package_data = {'dnspy': ['data/*']},
      license='Apache',
     )

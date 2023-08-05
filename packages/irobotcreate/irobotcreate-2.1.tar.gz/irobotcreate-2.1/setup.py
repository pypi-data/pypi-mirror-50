
from setuptools import setup, find_packages

setup(name              = 'irobotcreate',
      version           = '2.1',
      author            = 'Chris Cantrell',
      author_email      = 'topherCantrell@gmail.com',
      description       = 'Python code to control the irobotCreate2 from a raspberry pi',
      license           = 'MIT',
      classifiers       = [
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: MIT License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development',
               'Topic :: System :: Hardware'],
      url               = 'https://github.com/topherCantrell/robots-piCreate',  
      install_requires  = [      
        'serial'
      ],    
      packages          = find_packages())
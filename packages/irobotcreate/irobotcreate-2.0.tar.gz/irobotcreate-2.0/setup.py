
from setuptools import setup, find_packages

classifiers = ['Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: MIT License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development',
               'Topic :: System :: Hardware']

setup(name              = 'irobotcreate',
      version           = '2.0',
      author            = 'Chris Cantrell',
      author_email      = 'topherCantrell@gmail.com',
      description       = 'Python code to control the irobotCreate2 from a raspberry pi',
      license           = 'MIT',
      classifiers       = classifiers,
      url               = 'https://github.com/topherCantrell/robots-piCreate',  
      install_requires  = [      
        'serial'
      ],    
      packages          = find_packages())
from distutils.core import setup

setup(
    name = 'pybinarymoip',
    version = '0.0.2',
    license = 'MIT',
    description = 'Python library for Binary Media over IP (MOIP), used for Home Assistant',
    author = 'Greg J. Badros',
    author_email = 'badros@gmail.com',
    url = 'http://github.com/gjbadros/pywattbox',
    packages=['pybinarymoip'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Home Automation',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

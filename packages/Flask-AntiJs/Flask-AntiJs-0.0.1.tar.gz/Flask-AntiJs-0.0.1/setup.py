"""
Flask-AntiJs
-------------

Flask-AntiJs is a Flask extension the protects endpoints against
'undefined' javascript values by checking the URL, query params and payloads
and return a 400 (Bad request) response.
"""
from setuptools import setup

version="0.0.1"

setup(
    name='Flask-AntiJs',
    version=version,
    url='https://github.com/michaelbukachi/flask-antijs',
    license='BSD',
    author='Michael Bukachi',
    author_email='michaelbukachi@gmail.com',
    description='An extension to check \'undefined\' JS values',
    long_description=__doc__,
    py_modules=['flask_antijs'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    setup_requires=['pytest-runner', 'wheel', 'twine'],
    tests_require=['pytest', 'pytest-cov'],
    keywords='flask antijs',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

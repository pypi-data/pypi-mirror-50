"""
flask-theme
------------
flask-theme provides infrastructure for theming support in Flask
applications. It takes care of:

- Loading themes
- Rendering templates from themes
- Serving static files like CSS and images from themes


Links
`````
* `documentation <http://flask-theme.readthedocs.io/>`_
* `development version <https://github.com/liuliqiang/flask-theme>`_
"""

from setuptools import setup
import sys
requires = ['Flask>=0.6']
if sys.version_info < (2, 6):
    requires.append('simplejson')

setup(
    name='flask-theme',
    version='0.3.2',
    url='https://github.com/liuliqiang/flask-theme',
    license='MIT',
    author='Liqiang Lau',
    author_email='liqianglau@outlook.com',
    description='Provides infrastructure for theming Flask applications',
    long_description=__doc__,
    packages=['flask_theme'],
    py_modules=['flask_theme'],
    zip_safe=False,
    platforms='any',
    install_requires=requires,
    tests_require='nose',
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

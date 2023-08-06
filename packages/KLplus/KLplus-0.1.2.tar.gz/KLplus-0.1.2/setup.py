from setuptools import setup, find_packages
from os.path import join, dirname


base_dir = dirname(__file__)
version_ = {}

with open(join(base_dir, 'KLplus', '_version.py')) as f:
    exec(f.read(), version_)

with open(join(base_dir, "README.md")) as f:
    long_d = f.read()


setup(
    name = version_['__name__'],
    version = version_['__version__'],

    description = version_['__summary__'],
    long_description = long_d,
    long_description_content_type="text/markdown",
    license = version_['__license__'],
    url = version_['__uri__'],

    author = version_['__author__'],
    author_email = version_['__email__'],

    platforms = ['Linux'], # Somente para metadados

    packages = find_packages(),
    install_requires = ['python-xlib==0.25'],
    dependency_links = [
        'https://github.com/python-xlib/python-xlib/archive/0.25.tar.gz'
    ],
    
    zip_safe = False,

    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: Portuguese (Brazilian)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Logging'
    ]
)

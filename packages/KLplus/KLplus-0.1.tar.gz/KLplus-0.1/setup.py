from setuptools import setup
from os.path import join, dirname

def func_read(fname):
    with open(join(dirname(__file__), fname)) as f:
        return f.read()

setup(
    name='KLplus',
    python_requires='>=3.6',
    version='0.1',
    url='https://github.com/danbros/Plus_KLL.git',
    author='Dan Barros',
    author_email='dpb4fun@gmail.com',
    description=('A simple Keylogger for OS Linux'),
    long_description=func_read('README.md'),
    license='GPLv2',
    platforms=['Linux'],
    packages=['KLplus'],
    install_requires=['python-xlib>=0.25'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: Portuguese (Brazilian)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.7',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Logging',
    ]
)
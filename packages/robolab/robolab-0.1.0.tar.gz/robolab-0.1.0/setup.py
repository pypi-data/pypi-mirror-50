from os.path import abspath, join, dirname
from setuptools import setup


CURDIR = dirname(abspath(__file__))


with open(join(CURDIR, "VERSION")) as f:
    VERSION = f.read().strip()


with open(join(CURDIR, 'README.md')) as f:
    LONG_DESCRIPTION = f.read()


setup(
    name='robolab',
    version=VERSION,
    license='Apache License 2.0',
    keywords=['python', 'robotframework', 'rpa'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],

    author='Orlof',
    author_email='orlof@users.noreply.github.com',

    url='http://github.com/robocloud/robolab',

    packages=['robolab'],
    entry_points={'console_scripts': ['openrpa = robolab.Robolab:main']},

    description='Open source development tools for Robot Framework RPA developers',
    long_description=LONG_DESCRIPTION,
)

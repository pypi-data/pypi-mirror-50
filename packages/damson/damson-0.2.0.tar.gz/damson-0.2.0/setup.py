import os
import setuptools

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, 'damson', '__version__.py'), 'r') as f:
    exec (f.read(), about)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=about['__title__'],
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    keywords='Validation, verification and checking fields framework in python.',
    description=about['__description__'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xasync/damson",
    packages=setuptools.find_packages(exclude=('tests',)),
    license=about['__license__'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)

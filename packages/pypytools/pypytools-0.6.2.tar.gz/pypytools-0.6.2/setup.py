#   Copyright 2015-2018 Antonio Cuni anto.cuni@gmail.com

from setuptools import setup

desc = "A collection of useful tools to use PyPy-specific features, with CPython fallbacks"


setup(
    name="pypytools",
    version="0.6.2",
    author="Antonio Cuni",
    author_email="anto.cuni@gmail.com",
    url="http://bitbucket.org/antocuni/pypytools/",
    license="MIT X11 style",
    description=desc,
    packages=["pypytools", "pypytools.compat", "pypytools.gc",
              "pypytools.compat.micronumpy"],
    long_description=desc,
    install_requires=["py"],
)

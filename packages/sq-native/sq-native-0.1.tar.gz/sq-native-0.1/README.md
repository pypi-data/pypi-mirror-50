# Sqreen Native Python Module

[![Build status](https://badge.buildkite.com/d884ea8c5819a68324112977def52247f79bfac1d5fe294228.svg)](https://buildkite.com/sqreen/agentpythonnative)

The native libraries are added to this Python module with git submodules.

Build the binary wheel with:
```
pip install cmake
python setup.py bdist_wheel
```

Build the source package (without the libraries) with:
```
python setup.py sdist
```

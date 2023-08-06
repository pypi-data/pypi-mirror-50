# Meager

Meager is a tiny web framework built on the socketserver module in Python.

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/17b389bf6d6b40939dd39156b9525bb4)](https://app.codacy.com/app/ParanoidVoxel/meager)
[![Build Status](https://travis-ci.org/ParanoidVoxel/meager.svg?branch=master)](https://travis-ci.org/ParanoidVoxel/meager)
[![Python Versions](https://img.shields.io/pypi/pyversions/meager.svg)](https://pypi.python.org/pypi/meager)

## Installation

Meager is available on [PyPI](https://pypi.org/project/meager).

You can install meager using pip: `pip install meager`

## Examples

This is the simplest way of using meager, returning html upon a request to "/".

The module is heavily inspired by flask, and it's ease of use, and readability.

### Example returning html
```python
import meager
app = meager.Server(host="0.0.0.0", port=8080) # Set binding ip address and port, default is localhost:2090

@app.router.route("/")
def index(request):
    return "<h1>Hello world!</h1>"
app.serve()
```

### Example returning JSON
```python
import meager
app = meager.Server()
example_dict = {"key1": "val1", "key2": "val2"}

@app.router.route("/")
def index(request):
    return example_dict # It can detect if you're sending a dictionary
                        # and automatically changes the "Content-Type:" header to application/json 
app.serve()
```

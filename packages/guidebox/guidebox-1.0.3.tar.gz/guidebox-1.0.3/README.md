# guidebox-python

This is the python wrapper for the Guidebox API. See full Guidebox documentation [here](https://guidebox.com/docs/python). For best results, be sure that you're using [the latest version](https://guidebox.com/docs/python#version) of the Guidebox API and the latest version of the python wrapper.

This wrapper supports Python 2.6, 2.7, 3.3, 3.4, 3.5, 3.6, pypy, and pypy3 and works in the object oriented style. That is, to make calls you have to call the method on a class and the return types are python objects. To get a `dict` on any object, you can call the `to_dict()` method of the object.

## Table of Contents

- [Getting Started](#getting-started)
  - [Registration](#registration)
  - [Installation](#installation)
  - [Usage](#usage)
- [Testing](#testing)

## Getting Started

Here is the [Guidebox Documentation](https://api.guidebox.com/docs) and a general overview of the Guidebox services available, click through to read more.

### Registration

First, you will need to first create an account at [Guidebox](https://api.guidebox.com/register) and obtain your API Key.

Once you have created an account, you can access your API Keys from the [Keys Page](https://api.guidebox.com/docs/keys).

### Installation

You can use `pip` or `easy_install` for installing the package.

```
pip install guidebox
easy_install guidebox
```

To initialize the wrapper, import `guidebox` and set the `api_key`

```python
import guidebox
guidebox.api_key = 'your-api-key'

// set an api version (optional)
guidebox.api_version = 'api-version'
```

### Usage

We've provided an example script you can run in examples/ that has examples of how to use the guidebox-python wrapper with some of our core endpoints.

## Testing

Install all requirements with `pip install -r requirements.txt`.

You can run all tests with the command `nosetests` in the main directory.

=======================

Copyright (c) 2017 Guidebox

Released under the MIT License, which can be found in the repository in `LICENSE`.

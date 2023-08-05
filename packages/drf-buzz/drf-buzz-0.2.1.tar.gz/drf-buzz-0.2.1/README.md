[![Build Status](https://travis-ci.org/adalekin/drf-buzz.svg?branch=master)](https://travis-ci.org/adalekin/drf-buzz) [![Coverage Status](https://coveralls.io/repos/github/adalekin/drf-buzz/badge.svg?branch=master)](https://coveralls.io/github/adalekin/drf-buzz?branch=master)

drf-buzz
========

This is an extension of the [py-buzz](https://github.com/dusktreader/py-buzz)
package.

It adds extra functionality especially for DRF. Predominately, it adds the
ability to jsonify an exception

Installation
------------

```
pip install drf-buzz
```

Usage
-----

Add `drf-buzz` exception handler in `settings.py`:

```python
REST_FRAMEWORK = {
    ...
    'EXCEPTION_HANDLER': 'drf_buzz.exception_handler'
    ...
}
```

Use `py-buzz` exceptions in your DRF viewsets:

```python
import drf_buzz

from rest_framework import status, viewsets


class MyException(drf_buzz.DRFBuzz):
    status_code = status.BAD_REQUEST


class MyViewSet(viewsets.ViewSet):
    def list(self, request):
        raise MyException('Not implemented yet.')
```


Tests
-----

To run the test suite execute the following command in package root folder:

```
python setup.py test
```

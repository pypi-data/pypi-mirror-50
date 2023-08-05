import buzz

import rest_framework.exceptions
from rest_framework.views import exception_handler as base_exception_handler

import requests.exceptions

from . import utils


class DRFBuzz(buzz.Buzz, rest_framework.exceptions.APIException):
    def __init__(self, message, *format_args, **format_kwds):
        super().__init__(message=message, *format_args, **format_kwds)
        rest_framework.exceptions.APIException.__init__(self=self, detail=message, code=repr(self))


def exception_handler(exc, context):
    # FIXME: implicit requests dependency
    if isinstance(exc, requests.exceptions.HTTPError):
        try:
            response_data = exc.response.json()
        except ValueError:
            ...
        else:
            # Override an exception if it's a pretty enough
            if utils.is_pretty(response_data):
                status_code = exc.response.status_code

                exc = rest_framework.exceptions.APIException(detail=response_data)
                exc.status_code = status_code

    response = base_exception_handler(exc, context)

    if not response:
        exc = rest_framework.exceptions.APIException(exc)
        response = base_exception_handler(exc, context)

    if response is not None:
        if utils.is_pretty(response.data):
            return response

        data = {
            'code': exc.__class__.__name__
        }

        if 'detail' in response.data:
            description = response.data['detail']
        else:
            description = exc.default_detail
            data['fields'] = response.data

        data['description'] = description

        response.data = data

    return response

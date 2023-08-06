from collections import OrderedDict

from django.http import Http404
from django.views.generic import TemplateView

from rest_framework import exceptions as drf_exceptions
from rest_framework.views import exception_handler as drf_exception_handler

from . import exceptions
from .exception_handling import HandledException

ERROR_CONTENT_TYPE = 'application/problem+json'


def exception_handler(exc, context):
    """
    Transform 4xx and 5xx errors into DSO-compliant shape.
    """
    response = drf_exception_handler(exc, context)
    if response is None:
        return

    request = context.get('request')

    serializer = HandledException.as_serializer(exc, response, request)
    response.data = OrderedDict(serializer.data.items())
    # custom content type
    response['Content-Type'] = ERROR_CONTENT_TYPE
    return response


class ErrorDetailView(TemplateView):
    template_name = 'zds_schema/error_detail.html'

    def _get_exception_klass(self):
        klass = self.kwargs['exception_class']

        for module in [exceptions, drf_exceptions]:
            exc_klass = getattr(module, klass, None)
            if exc_klass is not None:
                return exc_klass
        else:
            raise Http404("Unknown exception class '{}'".format(klass))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exc_klass = self._get_exception_klass()
        context.update({
            'type': exc_klass.__name__,
            'status_code': exc_klass.status_code,
            'default_detail': exc_klass.default_detail,
            'default_code': exc_klass.default_code,
        })
        return context

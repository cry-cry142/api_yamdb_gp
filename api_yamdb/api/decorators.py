from rest_framework import status
from rest_framework.response import Response


def not_allowed_put_method(cls):
    upd = cls.update

    def update(self, request, *args, **kwargs):
        if self.action == 'update':
            response = {'detail': 'Method \"PUT\" not allowed.'}
            return Response(
                response, status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return upd(self, request, *args, **kwargs)

    cls.update = update
    return cls

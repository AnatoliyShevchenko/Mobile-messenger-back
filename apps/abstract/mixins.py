# Rest Framework
from rest_framework.response import Response

# Third-Party
from typing import Any

# Local
from settings.config.conf import STATUS_CODES


class ResponseMixin:
    """Mixin for Response."""

    def get_response(
        self, 
        key: str = 'default',
        data: dict[str: Any] = None, 
        status: str = None
    ) -> Response:
        """Return custom Response."""

        return Response(
            data={key : data},
            status=STATUS_CODES[status]
        )
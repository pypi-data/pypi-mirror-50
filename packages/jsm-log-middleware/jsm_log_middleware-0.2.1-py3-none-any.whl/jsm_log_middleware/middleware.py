import logging
import uuid

from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django_stomp.builder import build_publisher
from django_stomp.services.producer import do_inside_transaction
from jsm_user_services.services.user import get_user_access_as_id_from_jwt
from jsm_user_services.services.user import get_user_id_from_jwt
from request_id_django_log.request_id import current_request_id

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


logger = logging.getLogger(__name__)


class LogAudit(MiddlewareMixin):
    def process_request(self, request: WSGIRequest):

        if request.path == "/healthcheck/":
            return

        try:
            if request.path.split("/")[1] == "static":
                return

        except BaseException as e:
            pass

        application_name = getattr(settings, "LOG_APPLICATION_NAME", None)

        user_id = get_user_id_from_jwt()
        user_access_as = get_user_access_as_id_from_jwt()
        request_id = current_request_id()
        host = request.META.get("HTTP_HOST", "not-found")
        url = f"{request.scheme}://{host}{request.path}{request.GET.urlencode()}"
        body = request.body.decode("utf-8")

        data = {"session": request.session.session_key, "application_name": application_name}

        log_data = {
            "url": url,
            "body": body if body else None,
            "user_id": user_id,
            "request_id": request_id,
            "method": request.method,
            "user_access_as": user_access_as,
            "data": data,
        }

        try:

            publisher = build_publisher(f"audit-log-{uuid.uuid4()}")
            with do_inside_transaction(publisher):
                publisher.send(log_data, queue="/queue/audit-log")

            publisher.close()

        except BaseException as e:
            logger.warning("Error to send log_data %s", log_data)
            logger.exception(e)

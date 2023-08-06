#! -*- coding : utf-8 -*-

# Integration of Zope (4) with Sentry
# The code below is heavily based on the raven.contrib. zope module

import os
import logging
import sentry_sdk

from zope.component import adapter
from zope.globalrequest import getRequest
from AccessControl.users import nobody
from ZPublisher.interfaces import IPubFailure
from ZPublisher.HTTPRequest import _filterPasswordFields


sentry_dsn = os.environ.get("SENTRY_DSN")
if not sentry_dsn:
    raise RuntimeError("Environment variable SENTRY_DSN not configured")

def before_send(event, hint):

    return event

sentry_sdk.init(sentry_dsn, max_breadcrumbs=50, before_send=before_send, debug=False)
logging.info("Sentry integration enabled")


from sentry_sdk import configure_scope

with configure_scope() as scope:
    scope.user = {"email": "john.doe@example.com"}
    scope.set_tag("foo", "bar")


1/0

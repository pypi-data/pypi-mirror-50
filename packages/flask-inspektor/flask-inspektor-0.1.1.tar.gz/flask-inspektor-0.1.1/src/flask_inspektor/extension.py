from __future__ import absolute_import
from builtins import object
from future.utils import iteritems

import logging
from collections import defaultdict
from operator import itemgetter
from time import time

from flask import _request_ctx_stack, current_app
from sqlalchemy.engine import Engine
from sqlalchemy.event import listen, remove


log = logging.getLogger(__name__)


HEADER = 'X-QueryInspector'


def _filter_duplicates(queries):
    """
    Prepare a list of queries that were executed more than once.
    Ordered by execution count, descending.
    """
    result = {}

    for query, count in iteritems(queries):
        if count < 2:
            continue  # One instance is not a duplicate!
        result[query] = count

    return sorted(iteritems(result), key=itemgetter(1), reverse=True)


class QueryInspector(object):
    """
    Extension for a Flask app providing database metrics information.

    Lets the application log performed SQL queries and return SQL metrics
    in the response headers. Assumes SQLAlchemy use.
    """

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        """
        Initialise the extension for a given application.

        Arguments:
            app (flask.Flask): An instance of a running application.
        """
        # Set some safe and sane defaults.
        app.config.setdefault('QUERYINSPECT_ENABLED', False)
        app.config.setdefault('QUERYINSPECT_HEADERS', True)
        app.config.setdefault('QUERYINSPECT_LOG', True)
        app.config.setdefault('QUERYINSPECT_LOG_DUPES', False)

        # Only initialises and attaches itself when explicitly enabled.
        if not app.config.get('QUERYINSPECT_ENABLED', False):
            return
        else:
            log.info('Running with QueryInspector enabled')

        # Attach hooks to events interesting for this extension.
        app.before_request(self._before_request)
        app.after_request(self._after_request)

        # Expose for easy access on the application instance.
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['qi'] = self

    def _attach_sqla_hooks(self):
        """Attach to query-related events from SQLAlchemy."""
        listen(Engine, 'connect', self._on_connect)
        listen(Engine, 'before_cursor_execute', self._before_cursor_execute)
        listen(Engine, 'after_cursor_execute', self._after_cursor_execute)

    def _detach_sqla_hooks(self):
        """Clean up SQLAlchemy events attachment."""
        remove(Engine, 'connect', self._on_connect)
        remove(Engine, 'before_cursor_execute', self._before_cursor_execute)
        remove(Engine, 'after_cursor_execute', self._after_cursor_execute)

    @property
    def _store(self):
        """
        A data structure to store metrics.
        Accessed in a thread-safe and Flask-preferred way.
        """
        ctx = _request_ctx_stack.top
        if ctx is None:
            raise RuntimeError(
                'Cannot access metrics store outside of a request')

        if not hasattr(ctx, '_qi'):
            self._store = {}  # Use setter here for brevity.

        return ctx._qi

    @_store.setter
    def _store(self, data):
        ctx = _request_ctx_stack.top
        if ctx is None:
            raise RuntimeError(
                'Cannot access metrics store outside of a request')

        ctx._qi = data

    def _before_request(self, *args, **kwargs):
        """Initialise metrics structure."""
        self._store = {
            'r_start': time(),  # Request start.
            'q_start': 0,  # Current query start.
            'r_time': 0,  # Request time.
            'q_time': 0,  # Total querying time.
            'reads': 0,  # Read queries.
            'writes': 0,  # Write queries.
            'conns': 0,  # DB connections.
            'queries': defaultdict(int),  # Unique query count.
        }
        self._attach_sqla_hooks()

    def _on_connect(self, *args, **kwargs):
        """Count the number of *newly* opened connections."""
        self._store['conns'] += 1

    def _before_cursor_execute(self, conn, cursor, *args, **kwargs):
        """Record the timestamp of the beginning of a new SQL query."""
        self._store['q_start'] = time()

    def _after_cursor_execute(self, conn, cursor, statement, *args, **kwargs):
        """Record the time and the type of last SQL query execution."""
        store = self._store

        store['q_time'] += time() - store['q_start']

        if statement.lower().startswith('select'):
            store['reads'] += 1
        else:
            store['writes'] += 1

        # Gather specific query counts.
        store['queries'][statement] += 1

    def _after_request(self, response, *args, **kwargs):
        """Output metrics and clean up."""
        self._detach_sqla_hooks()
        store = self._store

        # Prepare summary metrics.
        store['q_time_ms'] = round(store['q_time'] * 1000, 1)
        store['r_time_ms'] = round((time() - store['r_start']) * 1000, 1)

        duplicate_queries = _filter_duplicates(store['queries'])
        store['duplicates'] = len(duplicate_queries)

        # Middle ground between human/machine readable.
        output = (
            'measure#qi.r_time={r_time_ms:.1f}ms, '
            'measure#qi.q_time={q_time_ms:.1f}ms, '
            'count#qi.reads={reads:d}, '
            'count#qi.writes={writes:d}, '
            'count#qi.conns={conns:d}, '
            'count#qi.duplicates={duplicates:d}'
            .format(**store)
        )

        if current_app.config.get('QUERYINSPECT_LOG'):
            log.info(output)

        if current_app.config.get('QUERYINSPECT_HEADERS'):
            response.headers[HEADER] = output

        if current_app.config.get('QUERYINSPECT_LOG_DUPES'):
            for query, count in duplicate_queries:
                log.warn('Duplicated query, executed %d times:\n%s',
                         count, query)

        # IMPORTANT
        return response

import six

from flask_sqlalchemy import SQLAlchemy

from flask_inspektor import QueryInspector
from tests.base import FakeAppTestCase


class QueryInspectBasicTest(FakeAppTestCase):
    def test_not_initialised_by_default(self):
        # Bootstrap the extension.
        QueryInspector(self.app)
        # Default configuration doesn't allow initialisation.
        extensions = getattr(self.app, 'extensions')
        self.assertNotIn('qi', extensions)

    def test_initialised(self):
        self.app.config['QUERYINSPECT_ENABLED'] = True
        QueryInspector(self.app)

        self.assertTrue(self.app.extensions['qi'])

    def test_initialised_lazy(self):
        qi = QueryInspector()

        self.app.config['QUERYINSPECT_ENABLED'] = True
        qi.init_app(self.app)

        self.assertTrue(self.app.extensions['qi'])


class QueryInspectTimingTest(FakeAppTestCase):
    def test_no_queries(self):
        self.app.config['QUERYINSPECT_ENABLED'] = True
        self.app.config['QUERYINSPECT_HEADERS'] = True
        QueryInspector(self.app)

        headers = self.client.get('/').headers
        self.assertIn('X-QueryInspector', headers)

        value = headers['X-QueryInspector']
        self.assertIn('count#qi.reads=0', value)
        self.assertIn('count#qi.writes=0', value)
        self.assertIn('count#qi.conns=0', value)

    def test_slow_view(self):
        self.app.config['QUERYINSPECT_ENABLED'] = True
        self.app.config['QUERYINSPECT_HEADERS'] = True
        QueryInspector(self.app)

        headers = self.client.get('/slow').headers
        value = headers['X-QueryInspector']

        six.assertRegex(self, value, r'measure#qi\.r_time=1[\d]{2}\.[\d]ms')


class QueryInspectSQLTest(FakeAppTestCase):
    def setUp(self):
        # Fake DB setup for testing ORM-related things.
        self.db = db = SQLAlchemy(self.app)

        class TestModel(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            foo = db.Column(db.String(8))
        self.Model = TestModel

        db.create_all(app=self.app)

    def test_db_reads(self):
        def _read_view():
            # Simulate SQL SELECT query.
            self.Model.query.first()
            return 'read'
        self.app.add_url_rule('/read', 'read', _read_view)

        self.app.config['QUERYINSPECT_ENABLED'] = True
        self.app.config['QUERYINSPECT_HEADERS'] = True
        QueryInspector(self.app)

        headers = self.client.get('/read').headers
        value = headers['X-QueryInspector']
        self.assertIn('count#qi.reads=1', value)

    def test_db_writes(self):
        def _write_view():
            # Simulate SQL INSERT query.
            m = self.Model(foo='bar')
            self.db.session.add(m)
            self.db.session.commit()
            return 'write'
        self.app.add_url_rule('/write', 'write', _write_view)

        self.app.config['QUERYINSPECT_ENABLED'] = True
        self.app.config['QUERYINSPECT_HEADERS'] = True
        QueryInspector(self.app)

        headers = self.client.get('/write').headers
        value = headers['X-QueryInspector']
        self.assertIn('count#qi.writes=1', value)

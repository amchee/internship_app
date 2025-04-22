import unittest
from app import create_app, db
from app.models import Internship, Application

class TestSystem(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()

    def test_user_flow_post_and_apply(self):
        response = self.client.post('/post', data={
            'title': 'Software Tester',
            'company': 'TestCorp',
            'description': 'QA and automation'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            internship = Internship.query.first()
            self.assertIsNotNone(internship)

        response = self.client.post(f'/apply/{internship.id}', data={
            'name': 'Amel Adzemi',
            'email': 'adzemi.amel@gmail.com'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            application = Application.query.filter_by(email='adzemi.amel@gmail.com').first()
            self.assertIsNotNone(application)
            self.assertEqual(application.name, 'Amel Adzemi')
            self.assertEqual(application.internship_id, internship.id)

if __name__ == '__main__':
    unittest.main()

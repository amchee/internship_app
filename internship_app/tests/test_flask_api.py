import unittest
from app import create_app, db
from app.models import Internship, Application

class TestFlaskAPI(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Available Internships', response.data)

    def test_post_internship_route(self):
        response = self.client.post('/post', data={
            'title': 'Software Tester',
            'company': 'TestCorp',
            'description': 'QA and automation'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            internship = Internship.query.first()
            self.assertIsNotNone(internship)
            self.assertEqual(internship.title, 'Software Tester')
            self.assertEqual(internship.company, 'TestCorp')
            self.assertEqual(internship.description, 'QA and automation')

    def test_apply_internship_route(self):
        with self.app.app_context():
            internship = Internship(title='Web Developer', company='Meta', description='Frontend Developer')
            db.session.add(internship)
            db.session.commit()
            internship_id = internship.id

        response = self.client.post(f'/apply/{internship_id}', data={
            'name': 'Amel',
            'email': 'adzemi.amel@gmail.com'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            application = Application.query.filter_by(email='adzemi.amel@gmail.com').first()
            self.assertIsNotNone(application)
            self.assertEqual(application.name, 'Amel')
            self.assertEqual(application.internship_id, internship_id)

if __name__ == '__main__':
    unittest.main()

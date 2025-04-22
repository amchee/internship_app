import unittest
from unittest.mock import patch
from app import create_app, db
from app.models import Internship

class TestMocks(unittest.TestCase):
    def setUp(self):
        app = create_app({
            'TESTING': True,
            'WTF_CSRF_ENABLED': False,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SQLALCHEMY_TRACK_MODIFICATIONS': False
        })
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

        db.create_all()

        internship = Internship(title="Test Internship", company="Test Company", description="Test Description")
        db.session.add(internship)
        db.session.commit()
        self.internship_id = internship.id

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @patch('app.routes.send_welcome_email') 
    def test_send_email(self, mock_send_email):
        response = self.app.post(f'/apply/{self.internship_id}', data={
            'name': 'Amel Adzemi',
            'email': 'adzemi.amel@gmail.com'
        }, follow_redirects=True)

        mock_send_email.assert_called_once_with('adzemi.amel@gmail.com')
        self.assertEqual(response.status_code, 200)

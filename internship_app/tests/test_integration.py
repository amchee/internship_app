import unittest
from app import create_app, db
from app.models import Internship, Application

class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SQLALCHEMY_TRACK_MODIFICATIONS': False
        })
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
        self.app_context.pop()

    def test_post_internship_to_db(self):
        internship = Internship(title='Data Analyst', company='Google', description='Analyze data stuff')
        db.session.add(internship)
        db.session.commit()

        saved = Internship.query.first()
        self.assertEqual(saved.company, 'Google')
        self.assertEqual(saved.title, 'Data Analyst')

    def test_application_to_existing_internship(self):
        internship = Internship(title='Web Dev', company='Meta', description='Frontend focus')
        db.session.add(internship)
        db.session.commit()

        application = Application(name='Amel Adzemi', email='adzemi.amel@gmail.com', internship_id=internship.id)
        db.session.add(application)
        db.session.commit()

        saved = Application.query.filter_by(internship_id=internship.id).first()
        self.assertEqual(saved.name, 'Amel Adzemi')
        self.assertEqual(saved.internship_id, internship.id)

if __name__ == '__main__':
    unittest.main()

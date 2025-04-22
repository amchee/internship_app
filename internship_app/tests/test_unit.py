import unittest
from app.models import Internship, Application

class TestModels(unittest.TestCase):

    def test_internship_creation(self):
        internship = Internship(title='Backend Intern', company='OpenAI', description='Work on cool stuff')
        self.assertEqual(internship.title, 'Backend Intern')
        self.assertEqual(internship.company, 'OpenAI')
        self.assertEqual(internship.description, 'Work on cool stuff')

    def test_application_creation(self):
        application = Application(name='Amel', email='adzemi.amel@gmail.com', internship_id=1)
        self.assertEqual(application.name, 'Amel')
        self.assertEqual(application.email, 'adzemi.amel@gmail.com')
        self.assertEqual(application.internship_id, 1)

if __name__ == '__main__':
    unittest.main()

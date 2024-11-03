import unittest
from unittest.mock import patch
from http import HTTPStatus
from io import BytesIO
from faker import Faker
from flaskr.app import app
from builder import FindIssueBuilder, IssueBuilder

fake = Faker()
class IssueIntegrationTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        app.testing = True
        
    def test_should_endpoint_create_an_issue(self):
        data = {
            'file': (BytesIO(b"Testing file"), 'testfile.txt'),
            'auth_user_id': fake.uuid4(),
            'auth_user_agent_id': fake.uuid4(),
            'subject': fake.word(),
            'description': fake.sentence()
        }
        expected_message = "Issue created successfully with ID"

        response = self.client.post('/issue/post', content_type='multipart/form-data', data=data)

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(response.json["message"], expected_message)

    @patch('flaskr.application.issue_service.Issue')
    def test_should_return_an_internal_server_error_in_post_process(self, IssueMock):
        IssueMock.return_value = SystemError("Some weird error 🤯")
        data = {
            'auth_user_id': fake.uuid4(),
            'auth_user_agent_id': fake.uuid4(),
            'subject': fake.word(),
            'description': fake.sentence()
        }
        error_message = "Error creating issue"

        response = self.client.post('/issue/post', content_type='application/json', json=data)

        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json["message"], error_message)

    
    def test_should_return_not_found_when_the_get_path_does_not_exist(self):
        data = {
            'auth_user_id': fake.uuid4(),
            'auth_user_agent_id': fake.uuid4(),
            'subject': fake.word(),
            'description': fake.sentence()
        }
        error_message = "Action not found"

        response = self.client.get('/issue/getFakePath', content_type='multipart/form-data', data=data)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.json["message"], error_message)
    
    def test_should_find_issue_by_user(self):
        user_id = fake.uuid4()
        data = {
            'auth_user_id': user_id,
            'auth_user_agent_id': fake.uuid4(),
            'subject': fake.word(),
            'description': fake.sentence()
        }
        expected_issue = IssueBuilder() \
                          .with_auth_user_id(data['auth_user_id']) \
                          .with_auth_user_agent_id(data['auth_user_agent_id']) \
                          .with_subject(data["subject"]) \
                          .with_description(data["description"]) \
                        .build()
        issues = []
        issues.append(expected_issue)
        expected_response = FindIssueBuilder().with_data(issues).build()

        self.client.post('/issue/post', content_type='multipart/form-data', data=data)
        response = self.client.get(f'/issues/find/{user_id}?page=1&limit=2')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json["page"], expected_response["page"])
        self.assertEqual(response.json["limit"], expected_response["limit"])
        self.assertEqual(response.json["total_pages"], expected_response["total_pages"])
        self.assertEqual(response.json["has_next"], expected_response["has_next"])
        self.assertEqual(response.json["data"][0]["auth_user_id"], expected_response["data"][0].auth_user_id)


        
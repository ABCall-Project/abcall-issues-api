import unittest
from flaskr.domain.models import IssueAttachment
from builder.IssueAttachmentBuilder import IssueAttachmentBuilder
from utils.testHelper import dict_to_obj

class IssueAttachmentUseCase(unittest.TestCase):

    def test_should_create_an_issue_attachment_an_convert_to_dictionary(self):
        issue_attachment_mock = IssueAttachmentBuilder().build()

        issue_attachment = IssueAttachment(issue_attachment_mock.id, issue_attachment_mock.issue_id, issue_attachment_mock.file_path)
        issue_attachment_dict = issue_attachment.to_dict()

        self.assertEqual(issue_attachment_dict['id'], str(issue_attachment_mock.id))
        self.assertEqual(issue_attachment_dict['issue_id'], str(issue_attachment_mock.issue_id))
        self.assertEqual(issue_attachment_dict['file_path'], str(issue_attachment_mock.file_path))
        
import unittest
from unittest.mock import patch, MagicMock
from flaskr.application.openAiService import OpenAIService

class TestOpenAIService(unittest.TestCase):

    @patch('requests.post')
    def test_ask_chatgpt_success(self, mock_post):
        """
        Test ask_chatgpt method when the API responds with a successful answer.
        """

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{'message': {'content': 'This is the answer from ChatGPT'}}]
        }
        mock_post.return_value = mock_response


        openai_service = OpenAIService()


        result = openai_service.ask_chatgpt("What is AI?")


        self.assertEqual(result, "This is the answer from ChatGPT")
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_ask_chatgpt_failure(self, mock_post):
        """
        Test ask_chatgpt method when the API responds with an error.
        """
 
        mock_response = MagicMock()
        mock_response.status_code = 500  # Simulating server error
        mock_post.return_value = mock_response

    
        openai_service = OpenAIService()


        result = openai_service.ask_chatgpt("What is AI?")


        self.assertIsNone(result)  
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_ask_chatgpt_exception(self, mock_post):
        """
        Test ask_chatgpt method when an exception occurs during the request.
        """

        mock_post.side_effect = Exception("Network error")


        openai_service = OpenAIService()

   
        result = openai_service.ask_chatgpt("What is AI?")


        self.assertIsNone(result)  
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_ask_chatgpt_invalid_json(self, mock_post):
        """
        Test ask_chatgpt method when the API returns an invalid JSON response.
        """
  
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")  
        mock_post.return_value = mock_response


        openai_service = OpenAIService()

 
        result = openai_service.ask_chatgpt("What is AI?")


        self.assertIsNone(result)  
        mock_post.assert_called_once()


    @patch('requests.post')
    def test_predictiveia_success(self, mock_post):
        """
        Test predictive ia method when the API responds with a successful answer.
        """

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'choices': [{'message': {'content': 'This is the answer from ChatGPT'}}]
        }
        mock_post.return_value = mock_response


        openai_service = OpenAIService()


        result = openai_service.ask_predictive_ai_chatgpt("What is AI?")


        self.assertEqual(result, "This is the answer from ChatGPT")
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_predicriveia_failure(self, mock_post):
        """
        Test predicrive ia response method when the API responds with an error.
        """
 
        mock_response = MagicMock()
        mock_response.status_code = 500  # Simulating server error
        mock_post.return_value = mock_response

    
        openai_service = OpenAIService()


        result = openai_service.ask_predictive_ai_chatgpt("What is AI?")


        self.assertIsNone(result)  
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_predictiveia_exception(self, mock_post):
        """
        Test ask_chatgpt method when an exception occurs during the request.
        """

        mock_post.side_effect = Exception("Network error")


        openai_service = OpenAIService()

   
        result = openai_service.ask_predictive_ai_chatgpt("What is AI?")


        self.assertIsNone(result)  
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_ask_predictiveia_invalid_json(self, mock_post):
        """
        Test ask_chatgpt method when the API returns an invalid JSON response.
        """
  
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")  
        mock_post.return_value = mock_response


        openai_service = OpenAIService()

 
        result = openai_service.ask_predictive_ai_chatgpt("What is AI?")


        self.assertIsNone(result)  
        mock_post.assert_called_once()


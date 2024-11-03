from datetime import date
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from http import HTTPStatus
import requests
import re
import os
import logging


class OpenAIService:
    """
    This class is for integrate the service with the OpenAI
    Attributes:
        base_url (string): the Auth api url 
    """

    def __init__(self):
        """
        service constructor 
        Args:
            
        """
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('default')
        self.logger.info('Instanced auth service')
        self.base_url = os.environ.get('OPENAI_API_PATH')
        self.token_openai = os.environ.get('TOKEN_OPENAI')


    def ask_chatgpt(self,question):
        """
        method to ask question to chat gpt
        Args:
            question (str): question to ask
        Return:
            answer (str): answer about ask
        """
        url = self.base_url
        headers = {
            'Authorization': f'Bearer {self.token_openai}',
            'Content-Type': 'application/json',
        }
        data = {
            'model': 'gpt-4o',  
            'messages': [{'role': 'user', 'content': question}],
        }
        
        try:
            self.logger.info(f'init consuming api openai {url}')
            response = requests.post(url, headers=headers, json=data)
            self.logger.info('quering open ai')
            if response.status_code == 200:
                self.logger.info('status code 200 quering open ai')
                answer = response.json()['choices'][0]['message']['content']
                return answer
            else:
                self.logger.info(f"error consuming open ai: {response.status_code}")
                return None
        except Exception as e:
            self.logger.info(f"Error comunication with open ai: {str(e)}")
            return None
        


    def ask_predictive_ai_chatgpt(self,context):
        """
        method to ask question to chat gpt to predict recomendations
        Args:
            context (str): context
        Return:
            answer (str): answer about ask
        """
        url = self.base_url
        headers = {
            'Authorization': f'Bearer {self.token_openai}',
            'Content-Type': 'application/json',
        }
        data = {
            'model': os.environ.get('OPENAI_PREDICTIVE_MODEL'),  
            'messages': [{'role': 'user', 'content': context}],
        }
        
        try:
            self.logger.info(f'init consuming api openai {url}')
            response = requests.post(url, headers=headers, json=data)
            self.logger.info('quering open ai')
            if response.status_code == 200:
                self.logger.info('status code 200 quering open ai')
                answer = response.json()['choices'][0]['message']['content']
                return answer
            else:
                self.logger.info(f"error consuming open ai: {response.status_code}")
                return None
        except Exception as e:
            self.logger.info(f"Error comunication with open ai: {str(e)}")
            return None
            

   
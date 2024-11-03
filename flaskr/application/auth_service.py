from datetime import date
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from http import HTTPStatus
import requests
import re
import os
import logging
from ..domain.models.auth_user_customer import AuthUserCustomer

class AuthService:
    """
    This class is for integrate the service with the Auth api
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
        self.logger.info(f'Instanced auth service')
        self.base_url = os.environ.get('AUTH_API_PATH')

    def get_users_by_customer_list(self,customer_id):
        """
        method to query all users associated to customer
        Args:
            none
        Return:
            auth_user_customer_list (AuthUserCustomer): list of auth users objects
        """
        auth_user_customer_list=[]
        try:
            
            self.logger.info(f'init consuming api auth {self.base_url}/users/getUsersByCustomer?customer_id={customer_id}')
            response = requests.get(f'{self.base_url}/users/getUsersByCustomer?customer_id={customer_id}')
            self.logger.info(f'quering users customer')
            if response.status_code == 200:
                self.logger.info(f'status code 200 quering users customer services')
                data = response.json()
                if data:
                    self.logger.info(f'there are auth response ')
                    for item in data:


                        auth_user_customer_list.append(AuthUserCustomer(item.get('id'),
                                item.get('auth_user_id'),
                                item.get('customer_id')                    
                        ))
 
                    self.logger.info(f'deserializing user  list')
                    return auth_user_customer_list
                    
                else:
                    self.logger.info(f'there arent users customer')
                    return None
            else:
                self.logger.info(f"error consuming user users auth api: {response.status_code}")
                return None
            
        except Exception as e:
            self.logger.info(f"Error comunication with auth api: {str(e)}")
            return None    
        

    def get_customer_by_user_id(self,user_id):
        """
        method to query user customer 
        Args:
            user_id: (str)
        Return:
            auth_user_customer (AuthUserCustomer):  auth user object
        """
        auth_user_customer=None
        try:
            
            self.logger.info(f'init consuming api auth {self.base_url}/users/getCompanyByUser?user_id={user_id}')
            response = requests.get(f'{self.base_url}/users/getCompanyByUser?user_id={user_id}')
            self.logger.info(f'quering users customer')
            if response.status_code == 200:
                self.logger.info(f'status code 200 quering users customer services')
                data = response.json()
                if data:
                    self.logger.info(f'there are auth response ')
                    auth_user_customer= AuthUserCustomer(data.get('id'),
                            data.get('auth_user_id'),
                            data.get('customer_id')                    
                    )
 
                    self.logger.info(f'deserializing user customer')
                    return auth_user_customer
                    
                else:
                    self.logger.info(f'there arent users customer')
                    return None
            else:
                self.logger.info(f"error consuming user users auth api: {response.status_code}")
                return None
            
        except Exception as e:
            self.logger.info(f"Error comunication with auth api: {str(e)}")
            return None  
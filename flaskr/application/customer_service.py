from datetime import date
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from http import HTTPStatus
import requests
import re
import os
import logging
from ..domain.models.customer import Customer
from ..domain.models.plan import Plan

class CustomerService:
    """
    This class is for integrate the service with the Customer api
    Attributes:
        base_url (string): the Customer api url 
    """

    def __init__(self):
        """
        service constructor 
        Args:
            
        """
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('default')
        self.logger.info('Instanced customer service')
        self.base_url = os.environ.get('CUSTOMER_API_PATH')

  
    def get_customer_by_id(self,customer_id):
        """
        method to query customer by id
        Args:
            customer_id: (uuid)
        Return:
            customer (Customer):  customer object
        """
        customer=None
        try:
            
            self.logger.info(f'init consuming api auth {self.base_url}/customer/getCustomerById?customer_id={customer_id}')
            response = requests.get(f'{self.base_url}/customer/getCustomerById?customer_id={customer_id}')
            self.logger.info('quering customer')
            if response.status_code == 200:
                self.logger.info('status code 200 quering customer services')
                data = response.json()
                if data:
                    self.logger.info('there are customer response ')
                    customer= Customer(
                        data.get('id'),
                        data.get('name'),
                        data.get('plan_id'),
                        data.get('date_suscription')                   
                    )
 
                    self.logger.info('deserializing customer')
                    return customer
                    
                else:
                    self.logger.info('there isnt customer')
                    return None
            else:
                self.logger.info(f"error consuming customer api: {response.status_code}")
                return None
            
        except Exception as e:
            self.logger.info(f"Error comunication with customer api: {str(e)}")
            return None  
        

    def get_plan_by_id(self,plan_id):
        """
        method to query plan by id
        Args:
            plan_id: (uuid)
        Return:
            plan (Plan):  Plan object
        """
        plan=None
        try:
            
            self.logger.info(f'init consuming api auth {self.base_url}/customer/getPlanById?plan_id={plan_id}')
            response = requests.get(f'{self.base_url}/customer/getPlanById?plan_id={plan_id}')
            self.logger.info('quering plan')
            if response.status_code == 200:
                self.logger.info('status code 200 quering plan services')
                data = response.json()
                if data:
                    self.logger.info('there are plan response ')
                    plan= Plan(
                        data.get('id'),
                        data.get('name'),
                        data.get('basic_monthly_rate'),
                        data.get('issue_fee')                   
                    )
 
                    self.logger.info('deserializing plan')
                    return plan
                    
                else:
                    self.logger.info('there isnt plan')
                    return None
            else:
                self.logger.info(f"error consuming plan api: {response.status_code}")
                return None
            
        except Exception as e:
            self.logger.info(f"Error comunication with plan api: {str(e)}")
            return None  
# -*- coding: utf-8 -*-
from pytyk.tyk_exceptions import AuthorizationError, InvalidTykInstance, InvalidPolicy, TykInternalError, InvalidTykOperation

import requests
from urllib.parse import urljoin
import json


class Tyk:

    def __init__(self, host, auth):
        self.host = host
        self.auth = auth

    def create_developer(self, email, passwd, org_id='', fields={}):
        response = self._request_create_developer(email, passwd, org_id, fields)
        if response.status_code == 200:
            return self._get_message(response)
        elif response.status_code == 400:
            return self._get_errors(response)
        elif response.status_code == 401:
            raise AuthorizationError()

    def create_key_for_developer(self, dev_id, policy_id):
        response = self._request_create_key_for_developer(dev_id, policy_id)
        if response.status_code == 200:
            key_id = self._get_message(response)
            return key_id
        elif response.status_code == 400:
            message = self._get_message(response)
            raise InvalidTykOperation(message=message)
        raise TykInternalError()

    def approve_key(self, key_id):
        response = self._request_key_approval(key_id)
        if response.status_code == 200:
            key = self._get_key(response)
            return key
        elif response.status_code == 400:
            message = self._get_message(response)
            raise InvalidTykOperation(message=message)
        raise TykInternalError()

    def set_password(self, dev_id, new_pass):
        response = self._request_new_password(dev_id, new_pass)
        if response.status_code == 200:
            status = self._get_status(response)
            return status
        elif response.status_code == 400:
            message = self._get_message(response)
            raise InvalidTykOperation(message=message)
        raise TykInternalError()

    def _request_create_developer(self, email, passwd, org_id, fields):
        url = self._get_url('developers')
        payload = {'email': email, 
                    'password': passwd, 
                    'org_id': org_id,
                    'fields': fields}
        response = self._make_post_request(url, payload)
        return response

    def _request_create_key_for_developer(self, dev_id, policy_id):
        url = self._get_url('requests')
        payload = {'by_user': dev_id, 'for_plan': policy_id, 'version': 'v2'}
        response = self._make_post_request(url, payload)
        return response

    def _request_key_approval(self, key_id):
        endpoint = 'requests/approve/%s' %(key_id)
        url = self._get_url(endpoint)
        response = self._make_put_request(url)
        return response

    def _request_new_password(self, dev_id, new_pass):
        endpoint = 'developers/password/%s' %(dev_id)
        url = self._get_url(endpoint)
        payload = { "password": new_pass }
        response = self._make_post_request(url, payload)
        return response
        
    def _make_post_request(self, url, payload):
        json_payload = json.dumps(payload)
        try:
            response = requests.post(url, data=json_payload, 
                                        headers={'Authorization': self.auth,
                                        'Content-Type': 'Application/json'})
            return response
        except ConnectionError:
            raise InvalidTykInstance()

    def _make_put_request(self, url):
        try:
            response = requests.put(url, headers={'Authorization': self.auth,
                                        'Content-Type': 'Application/json'})
            return response
        except ConnectionError:
            raise InvalidTykInstance()

    def _get_url(self, endpoint):
        return urljoin(self.host, 'api/portal/%s' %(endpoint))

    def _get_message(self, response):
        result = response.json()
        message = result['Message']
        return message

    def _get_status(self, response):
        result = response.json()
        status = result['Status']
        return status

    def _get_key(self, response):
        result = response.json()
        message = result['RawKey']
        return message

    def _get_errors(self, response):
        result = response.json()
        errors = result['Errors']
        return ','.join(errors)




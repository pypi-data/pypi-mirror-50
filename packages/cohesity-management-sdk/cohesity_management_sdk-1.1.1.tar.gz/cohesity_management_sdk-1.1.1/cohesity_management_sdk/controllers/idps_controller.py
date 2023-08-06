# -*- coding: utf-8 -*-
# Copyright 2019 Cohesity Inc.

import logging
from cohesity_management_sdk.api_helper import APIHelper
from cohesity_management_sdk.configuration import Configuration
from cohesity_management_sdk.controllers.base_controller import BaseController
from cohesity_management_sdk.http.auth.auth_manager import AuthManager
from cohesity_management_sdk.models.idp_service_configuration import IdpServiceConfiguration
from cohesity_management_sdk.exceptions.request_error_error_exception import RequestErrorErrorException

class IdpsController(BaseController):

    """A Controller to access Endpoints in the cohesity_management_sdk API."""

    def __init__(self, client=None, call_back=None):
        super(IdpsController, self).__init__(client, call_back)
        self.logger = logging.getLogger(__name__)

    def update_idp(self,
                   id,
                   body=None):
        """Does a PUT request to /public/idps/{id}.

        Returns the updated IdP configuration.

        Args:
            id (long|int): Specifies the Id assigned for the IdP Service by
                the Cluster.
            body (UpdateIdpConfigurationRequest, optional): Request to update
                an Idp Configuration.

        Returns:
            IdpServiceConfiguration: Response from the API. Success

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('update_idp called.')

            # Validate required parameters
            self.logger.info('Validating required parameters for update_idp.')
            self.validate_parameters(id=id)

            # Prepare query URL
            self.logger.info('Preparing query URL for update_idp.')
            _url_path = '/public/idps/{id}'
            _url_path = APIHelper.append_url_with_template_parameters(_url_path, {
                'id': id
            })
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)

            # Prepare headers
            self.logger.info('Preparing headers for update_idp.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }

            # Prepare and execute request
            self.logger.info('Preparing and executing request for update_idp.')
            _request = self.http_client.put(_query_url, headers=_headers, parameters=APIHelper.json_serialize(body))
            AuthManager.apply(_request)
            _context = self.execute_request(_request, name = 'update_idp')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for update_idp.')
            if _context.response.status_code == 0:
                raise RequestErrorErrorException('Error', _context)
            self.validate_response(_context)

            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, IdpServiceConfiguration.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def delete_idp(self,
                   id):
        """Does a DELETE request to /public/idps/{id}.

        Returns Success if the IdP configuration is deleted.

        Args:
            id (long|int): Specifies the Id assigned for the IdP Service by
                the Cluster.

        Returns:
            void: Response from the API. No Content

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('delete_idp called.')

            # Validate required parameters
            self.logger.info('Validating required parameters for delete_idp.')
            self.validate_parameters(id=id)

            # Prepare query URL
            self.logger.info('Preparing query URL for delete_idp.')
            _url_path = '/public/idps/{id}'
            _url_path = APIHelper.append_url_with_template_parameters(_url_path, {
                'id': id
            })
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)

            # Prepare and execute request
            self.logger.info('Preparing and executing request for delete_idp.')
            _request = self.http_client.delete(_query_url)
            AuthManager.apply(_request)
            _context = self.execute_request(_request, name = 'delete_idp')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for delete_idp.')
            if _context.response.status_code == 0:
                raise RequestErrorErrorException('Error', _context)
            self.validate_response(_context)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_idp_login(self,
                      tenant_id=None):
        """Does a GET request to /public/idps/login.

        Redirects the client to the IdP site with the URI to login.

        Args:
            tenant_id (string, optional): Specifies an optional tenantId for
                which the SSO login should be done. If this is not specified,
                Cluster SSO login is done.

        Returns:
            void: Response from the API.

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_idp_login called.')

            # Prepare query URL
            self.logger.info('Preparing query URL for get_idp_login.')
            _url_path = '/public/idps/login'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'tenantId': tenant_id
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)

            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_idp_login.')
            _request = self.http_client.get(_query_url)
            AuthManager.apply(_request)
            _context = self.execute_request(_request, name = 'get_idp_login')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for get_idp_login.')
            if _context.response.status_code == 0:
                raise RequestErrorErrorException('Error', _context)
            self.validate_response(_context)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def create_idp(self,
                   body=None):
        """Does a POST request to /public/idps.

        Returns the newly created IdP configuration.

        Args:
            body (CreateIdpConfigurationRequest, optional): Request to create
                a new IdP Configuration.

        Returns:
            IdpServiceConfiguration: Response from the API. Success

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('create_idp called.')

            # Prepare query URL
            self.logger.info('Preparing query URL for create_idp.')
            _url_path = '/public/idps'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_url = APIHelper.clean_url(_query_builder)

            # Prepare headers
            self.logger.info('Preparing headers for create_idp.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }

            # Prepare and execute request
            self.logger.info('Preparing and executing request for create_idp.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(body))
            AuthManager.apply(_request)
            _context = self.execute_request(_request, name = 'create_idp')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for create_idp.')
            if _context.response.status_code == 0:
                raise RequestErrorErrorException('Error', _context)
            self.validate_response(_context)

            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, IdpServiceConfiguration.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_idps(self,
                 names=None,
                 ids=None,
                 tenant_ids=None):
        """Does a GET request to /public/idps.

        Returns the Idps configured on the Cohesity Cluster corresponding to
        the filter parameters. If no filter is given, all Idp configurations
        are returned.

        Args:
            names (list of string, optional): Specifies the names of the IdP
                vendors like Okta. If specified, returns IdP configurations of
                the vendors matching the names in the parameters.
            ids (list of long|int, optional): Specifies the Ids of the IdP
                configuration. If specified, returns IdP configurations of the
                matching Ids in the IdP configuration.
            tenant_ids (list of string, optional): Specifies the Tenant Ids
                having IdP configurations. If specified, returns IdP
                configurations used by the tenants matching the Tenant Ids in
                the parameters.

        Returns:
            list of IdpServiceConfiguration: Response from the API. Success

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_idps called.')

            # Prepare query URL
            self.logger.info('Preparing query URL for get_idps.')
            _url_path = '/public/idps'
            _query_builder = Configuration.get_base_uri()
            _query_builder += _url_path
            _query_parameters = {
                'names': names,
                'ids': ids,
                'tenantIds': tenant_ids
            }
            _query_builder = APIHelper.append_url_with_query_parameters(_query_builder,
                _query_parameters, Configuration.array_serialization)
            _query_url = APIHelper.clean_url(_query_builder)

            # Prepare headers
            self.logger.info('Preparing headers for get_idps.')
            _headers = {
                'accept': 'application/json'
            }

            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_idps.')
            _request = self.http_client.get(_query_url, headers=_headers)
            AuthManager.apply(_request)
            _context = self.execute_request(_request, name = 'get_idps')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for get_idps.')
            if _context.response.status_code == 0:
                raise RequestErrorErrorException('Error', _context)
            self.validate_response(_context)

            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, IdpServiceConfiguration.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

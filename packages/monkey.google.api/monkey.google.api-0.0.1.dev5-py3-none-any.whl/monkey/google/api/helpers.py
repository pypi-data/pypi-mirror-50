#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os.path
import pickle

import googleapiclient.discovery
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError


class CredentialProvider(object):
    def __init__(self, scopes, credential_file, token_file):
        credentials = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                credentials = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credential_file, scopes)
                credentials = flow.run_local_server()
            # Save the credentials for the next run
            with open(token_file, 'wb') as token:
                dump = pickle.dump(credentials, token)
                print(dump)
        self.credentials = credentials

    def authorize(self, http):
        return self.credentials.authorize(http)


class GoogleAPIError(Exception):

    def __init__(self, message='Google API error', cause=None):
        self.message = message
        self.cause = cause


class GSuiteService:

    def __init__(self, name, version, credential_provider: CredentialProvider):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.name = name
        self.version = version
        self.credential_provider = credential_provider
        self.service = googleapiclient.discovery.build(self.name, self.version,
                                                       credentials=self.credential_provider.credentials)

    def list_all(self):
        raise NotImplemented()


class PeopleService(GSuiteService):

    def __init__(self, credential_provider: CredentialProvider):
        super().__init__('people', 'v1', credential_provider)

    def list_all(self):
        raise NotImplementedError()


class SheetService(GSuiteService):

    def __init__(self, credential_provider: CredentialProvider):
        super().__init__('sheets', 'v4', credential_provider)

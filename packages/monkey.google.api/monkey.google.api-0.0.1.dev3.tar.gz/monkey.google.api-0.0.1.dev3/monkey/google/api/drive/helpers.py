#!/usr/bin/python
# -*- coding: utf-8 -*-

from monkey.google.api.helpers import GSuiteService, CredentialProvider, GoogleAPIError
from googleapiclient.errors import HttpError


class DriveService(GSuiteService):
    def __init__(self, credential_provider: CredentialProvider):
        super().__init__('drive', 'v3', credential_provider)

    def create(self, request_id, drive_name):
        body = {
            'name': drive_name
        }
        try:
            result = self.service.drives().create(requestId=request_id, body=body).execute()
            return result
        except HttpError as e:
            raise GoogleAPIError('Unexpected error.', e)

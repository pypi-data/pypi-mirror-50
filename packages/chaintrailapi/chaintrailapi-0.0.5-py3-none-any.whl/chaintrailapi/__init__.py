import os
import requests_toolbelt
from requests_toolbelt import sessions

name = 'chaintrailapi'
# TODO implement API key authentication
API_BASE_URL = os.environ.get('CHAINTRAIL_BASE_URL')
session = sessions.BaseUrlSession(base_url=API_BASE_URL)

from .accounts import Account

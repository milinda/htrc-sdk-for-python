__author__ = 'Milinda Pathirage'

import os
import io
import urllib
import urllib2
import tempfile
import utils


class DataAPIClient:

    def __init__(self, endpoint=None, client_id=None, client_secret=None, token_endpoint=None):
        if endpoint is None:
            self.endpoint = os.environ['HTRC_IPYTHON_DATAAPI_EPR']
        else:
            self.endpoint = endpoint

        if client_id is None:
            self.client_id = os.environ['HTRC_IPYTHON_OAUTH2_CLIENT_ID']
        else:
            self.client_id = client_id

        if client_secret is None:
            self.client_secret = os.environ['HTRC_IPYTHON_OAUTH2_CLIENT_SECRET']
        else:
            self.client_secret = client_secret

        if token_endpoint is None:
            self.token_endpoint = os.environ['HTRC_IPYTHON_OAUTH2_TOKEN_ENDPOINT']
        else:
            self.token_endpoint = token_endpoint

    def get_volumes(self, volume_list, access_token=None):
        if access_token is None:
            access_token = utils.get_oauth2_token(self.token_endpoint, self.client_id, self.client_secret)

        headers = {"Authorization": "Bearer " + access_token,
                   "Content-type": "application/x-www-form-urlencoded"}

        volume_id_list = '|'.join(volume_list)
        parameters = {'volumeIDs': volume_id_list}
        body = urllib.urlencode(parameters)
        request_epr = self.endpoint + "/volumes"

        req = urllib2.Request(request_epr, body, headers)

        response = urllib2.urlopen(req)

        if response.code != 200:
            raise urllib2.HTTPError(response.url, response.code, response.read(), response.info(), response.fp)

        zip_content = io.BytesIO(response.read())

        temp_dir = tempfile.mkdtemp()

        utils.unzip(zip_content, temp_dir)

        return temp_dir



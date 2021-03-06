"""
A meta-provider that performs file actions on many different storage hosts, using waterbutler as an intermediary
"""
import typing
import urllib.parse

from ..base import OauthBaseProvider
import settings


class WBProvider(OauthBaseProvider):
    """A wrapper that uses the WB API to talk to one of a range of storage providers"""
    # Default name, but prefer users to pass it in explicitly (because this is sort of an indirect provider)
    NAME = 'waterbutler'

    BASE_URL = settings.WB_HOST
    DEFAULT_CREDENTIAL = settings.WATERBUTLER_OSF_TOKEN

    # True of osfstorage, but less so if using WB to talk to other providers. We allow the attempt and defer to
    #   WB's abstraction
    ALLOWS_SUBFOLDERS = True

    async def create_folder(self, foldername: str) -> typing.Tuple[str, int]:
        """Create a folder on that provider, & return the remote name/ id of the parent (to be used in future calls)"""

        # If a parent folder is specified, append it to the URL. Otherwise just add a trailing slash.
        parent_folder = self.parent_folder or '/'
        url = urllib.parse.urljoin(self.BASE_URL,
                                   f'/v1/resources/{settings.OSF_NODE}/providers/{self.provider_name}{parent_folder}')
        params = {
            'kind': 'folder',
            'name': foldername
        }
        resp, code = await self.make_request_get_json('PUT', url, params=params, headers={'Content-Type': 'application/json'})
        rv = resp['data']['attributes']['path'] if code < 400 else resp
        return rv, code

    async def upload_file(self, filename: str, content):

        # If a parent folder is specified, append it to the URL. Otherwise just add a trailing slash.
        parent_folder = self.parent_folder or '/'
        url = urllib.parse.urljoin(self.BASE_URL,
                                   f'/v1/resources/{settings.OSF_NODE}/providers/{self.provider_name}{parent_folder}')
        params = {
            'kind': 'file',
            'name': filename
        }
        return await self.make_request_get_json('PUT', url, params=params, data=content)

    @staticmethod
    def extract_uploaded_filename(payload: dict=None):
        return payload['data']['attributes']['name']

from urllib.parse import quote

import requests
from . import settings
from . import exceptions

__all__ = ("LinkedinAPI", "ProfileAPI", "ShareAPI", "OrganizationAPI")


class LinkedinAPI(object):

    def __init__(self, token, api_url=settings.LINKEDIN_API_URL, api_version=settings.LINKEDIN_API_VERSION):
        self.token = token
        self.api_url = "%s%s" % (api_url, api_version)

    @property
    def headers(self):
        return {
            'X-Restli-Protocol-Version': '2.0.0',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % self.token
        }

    def _make_get(self, url):
        r = requests.get(url, headers=self.headers)
        if not r.ok:
            msg = r.json().get('message', 'Unknown error')
            raise exceptions.BaseLinkedinException(msg)
        return r.json()

    def _make_post(self, url, json_data):
        r = requests.post(url, headers=self.headers, json=json_data)
        if not r.ok:
            msg = r.json().get('message', 'Unknown error')
            raise exceptions.BaseLinkedinException(msg)
        return r.json()

    def make_request(self, method, url, data=None, exception=exceptions.BaseLinkedinException):

        try:
            if method.lower() == 'get':
                return self._make_get(url)

            if method.lower() == 'post':
                return self._make_post(url=url, json_data=data)
        except exceptions.BaseLinkedinException as e:
            raise exception(str(e))


class ProfileAPI(LinkedinAPI):
    def get_profile(self):
        url = "%s/me" % self.api_url
        return self.make_request(method='get', url=url, exception=exceptions.ProfileException)


class OrganizationAPI(LinkedinAPI):

    def get_my_companies(self):
        url = '%s/organizationalEntityAcls?q=roleAssignee' % self.api_url
        return self.make_request(method='get', url=url, exception=exceptions.OrganizationException)


class ShareAPI(LinkedinAPI):
    def create(self, author, text):
        url = '%s/ugcPosts' % self.api_url
        post_data = {
            "author": author,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "NONE"
                },
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            },
        }
        return self.make_request(method='post', url=url, data=post_data, exception=exceptions.ShareException)

    def retrieve(self, post_urn):
        url = '%s/socialActions/%s' % (self.api_url, quote(post_urn))
        return self.make_request(method='get', url=url, exception=exceptions.ShareException)

from urllib.parse import urlencode

from django.conf import settings
from django.core import signing
from django.views.generic import RedirectView

NAVER_CALLBACK_URL = '/naver/callback/'
NAVER_STATE = 'naver_login'
NAVER_LOGIN_URL = 'https://nid.naver.com/oauth2.0/authorize'

class NaverLoginRedirectView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        domain = self.request.scheme + '://' + self.request.META.get('HTTP_HOST','')

        callback_url = domain + NAVER_CALLBACK_URL
        state = signing.dumps(NAVER_STATE)

        params = {
            'response_type': 'code',
            'client_id': settings.NAVER_CLIENT_ID,
            'redirect_uri': callback_url,
            'state': state
        }

        return f'{NAVER_LOGIN_URL}?{urlencode(params)}'


# https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id=클라이언트_아이디&redirect_uri=http://localhost:8000/naver/callback/&state=abc
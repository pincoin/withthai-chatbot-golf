import jwt
import requests
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

from .provider import LineProvider


class LineOAuth2Adapter(OAuth2Adapter):
    provider_id = LineProvider.id
    access_token_url = 'https://api.line.me/oauth2/v2.1/token'
    authorize_url = 'https://access.line.me/oauth2/v2.1/authorize'
    profile_url = 'https://api.line.me/v2/profile'

    decoded_email = ''

    def parse_token(self, data):
        token = super(LineOAuth2Adapter, self).parse_token(data)

        app = self.get_provider().get_app(request=None)

        id_token = data.get('id_token', '')

        decoded_id_token = jwt.decode(id_token,
                                      app.secret,
                                      audience=app.client_id,
                                      issuer='https://access.line.me',
                                      algorithms=['HS256'])

        self.decoded_email = decoded_id_token['email']

        return token

    def complete_login(self, request, app, token, **kwargs):
        headers = {'Authorization': 'Bearer {0}'.format(token.token)}
        resp = requests.get(self.profile_url, headers=headers)
        extra_data = resp.json()
        extra_data['email'] = self.decoded_email
        return self.get_provider().sociallogin_from_response(request,
                                                             extra_data)


oauth2_login = OAuth2LoginView.adapter_view(LineOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(LineOAuth2Adapter)

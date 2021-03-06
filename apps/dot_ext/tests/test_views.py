import json
import base64

from django.utils import timezone
from datetime import timedelta

from django.core.urlresolvers import reverse

from oauth2_provider.compat import parse_qs, urlparse
from oauth2_provider.scopes import get_scopes_backend
from oauth2_provider.models import AccessToken

from apps.test import BaseApiTest
from ..models import Application


class TestApplicationUpdateView(BaseApiTest):
    def test_update_form_show(self):
        """
        """
        read_group = self._create_group('read')
        self._create_capability('Read-Scope', [], read_group)
        write_group = self._create_group('write')
        self._create_capability('Write-Scope', [], write_group)
        # create user and add it to the read group
        user = self._create_user('john', '123456')
        user.groups.add(read_group)
        # create an application
        app = self._create_application('john_app', user=user)
        # render the edit view for the app
        self.client.login(username=user.username, password='123456')
        uri = reverse('oauth2_provider:update', args=[app.pk])
        response = self.client.get(uri)
        self.assertEqual(response.status_code, 200)


class TestAuthorizationView(BaseApiTest):
    def test_post_with_restricted_scopes_issues_token_with_same_scopes(self):
        """
        Test that when user unchecks some of the scopes the token is issued
        with the checked scopes only.
        """
        # create a user
        self._create_user('anna', '123456')
        # create a couple of capabilities
        capability_a = self._create_capability('Capability A', [])
        capability_b = self._create_capability('Capability B', [])
        # create an application and add capabilities
        application = self._create_application(
            'an app', grant_type=Application.GRANT_AUTHORIZATION_CODE,
            redirect_uris='http://example.it')
        application.scope.add(capability_a, capability_b)
        # user logs in
        self.client.login(username='anna', password='123456')
        # post the authorization form with only one scope selected
        payload = {
            'client_id': application.client_id,
            'response_type': 'code',
            'redirect_uri': 'http://example.it',
            'scope': ['capability-a'],
            'expires_in': 86400,
            'allow': True,
        }
        response = self.client.post(reverse('oauth2_provider:authorize'), data=payload)
        self.assertEqual(response.status_code, 302)
        # now extract the authorization code and use it to request an access_token
        query_dict = parse_qs(urlparse(response['Location']).query)
        authorization_code = query_dict.pop('code')
        token_request_data = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': 'http://example.it',
            'client_id': application.client_id,
        }
        response = self.client.post(reverse('oauth2_provider:token'), data=token_request_data)
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content.decode("utf-8"))
        # and here we test that only the capability-a scope has been issued
        self.assertEqual(content['scope'], "capability-a")


class TestTokenView(BaseApiTest):
    test_uuid = "0123456789abcdefghijklmnopqrstuvwxyz"
    test_username = "9abcdefghijklmnopqrstuvwxyz"

    def _create_test_token(self, user, application):

        now = timezone.now()
        expires = now + timedelta(days=1)

        scope = get_scopes_backend().get_available_scopes(application)

        t = AccessToken.objects.create(user=user, application=application,
                                       token="sample-token-string",
                                       expires=expires,
                                       scope=' '.join(scope))
        return t

    def _create_authorization_header(self, client_id, client_secret):
        return "Basic {0}".format(base64.b64encode("{0}:{1}".format(client_id, client_secret).encode('utf-8')).decode('utf-8'))

    def _create_authentication_header(self, username):
        return "SLS {0}".format(base64.b64encode(username.encode('utf-8')).decode("utf-8"))

    def test_get_tokens_success(self):
        anna = self._create_user(self.test_username, '123456')
        # create a couple of capabilities
        capability_a = self._create_capability('token_management', [['GET', '/v1/o/tokens/']], default=False)
        # create an application and add capabilities
        application = self._create_application(
            'an app', grant_type=Application.GRANT_AUTHORIZATION_CODE,
            redirect_uris='http://example.it')
        application.scope.add(capability_a)
        tkn = self._create_test_token(anna, application)
        response = self.client.get(reverse('token_management:token-list'),
                                   HTTP_AUTHORIZATION=self._create_authorization_header(application.client_id,
                                                                                        application.client_secret),
                                   HTTP_X_AUTHENTICATION=self._create_authentication_header(self.test_uuid))
        self.assertEqual(response.status_code, 200)
        result = response.json()
        expected = [{
            'id': tkn.id,
            'user': anna.id,
            'application': {
                'id': application.id,
                'name': 'an app',
                'logo_uri': '',
                'tos_uri': '',
                'policy_uri': '',
                'contacts': ''
            },
        }]
        self.assertEqual(result, expected)

    def test_delete_token_success(self):
        anna = self._create_user(self.test_username, '123456')
        # create a couple of capabilities
        capability_a = self._create_capability('token_management', [['DELETE', '/v1/o/tokens/\d+/']], default=False)
        # create an application and add capabilities
        application = self._create_application(
            'an app', grant_type=Application.GRANT_AUTHORIZATION_CODE,
            redirect_uris='http://example.it')
        application.scope.add(capability_a)
        tkn = self._create_test_token(anna, application)
        response = self.client.delete(reverse('token_management:token-detail', args=[tkn.pk]),
                                      HTTP_AUTHORIZATION=self._create_authorization_header(application.client_id,
                                                                                           application.client_secret),
                                      HTTP_X_AUTHENTICATION=self._create_authentication_header(self.test_uuid))
        self.assertEqual(response.status_code, 204)
        failed_response = self.client.delete(reverse('token_management:token-detail', args=[tkn.pk]),
                                             HTTP_AUTHORIZATION=self._create_authorization_header(application.client_id,
                                                                                                  application.client_secret),
                                             HTTP_X_AUTHENTICATION=self._create_authentication_header(self.test_uuid))
        self.assertEqual(failed_response.status_code, 404)

    def test_create_token_fail(self):
        self._create_user(self.test_username, '123456')

        # create a couple of capabilities
        capability_a = self._create_capability('token_management', [['POST', '/v1/o/tokens/']], default=False)
        # create an application and add capabilities
        application = self._create_application(
            'an app', grant_type=Application.GRANT_AUTHORIZATION_CODE,
            redirect_uris='http://example.it')
        application.scope.add(capability_a)
        response = self.client.post(reverse('token_management:token-list'),
                                    HTTP_AUTHORIZATION=self._create_authorization_header(application.client_id,
                                                                                         application.client_secret),
                                    HTTP_X_AUTHENTICATION=self._create_authentication_header(self.test_uuid))
        self.assertEqual(response.status_code, 405)

    def test_update_token_fail(self):
        anna = self._create_user(self.test_username, '123456')
        # create a couple of capabilities
        capability_a = self._create_capability('token_management', [['PUT', '/v1/o/tokens/\d+/']], default=False)
        # create an application and add capabilities
        application = self._create_application(
            'an app', grant_type=Application.GRANT_AUTHORIZATION_CODE,
            redirect_uris='http://example.it')
        application.scope.add(capability_a)
        tkn = self._create_test_token(anna, application)
        response = self.client.put(reverse('token_management:token-detail', args=[tkn.pk]),
                                   HTTP_AUTHORIZATION=self._create_authorization_header(application.client_id,
                                                                                        application.client_secret),
                                   HTTP_X_AUTHENTICATION=self._create_authentication_header(self.test_uuid))
        self.assertEqual(response.status_code, 405)

    def test_unauthorized_fail(self):
        anna = self._create_user(self.test_username, '123456')
        # create a couple of capabilities
        self._create_capability('token_management', [['GET', '/v1/o/tokens/']], default=False)
        # create an application and add capabilities
        application = self._create_application(
            'an app', grant_type=Application.GRANT_AUTHORIZATION_CODE,
            redirect_uris='http://example.it')
        self._create_test_token(anna, application)

        response = self.client.get(reverse('token_management:token-list'),
                                   HTTP_AUTHORIZATION=self._create_authorization_header(application.client_id,
                                                                                        application.client_secret),
                                   HTTP_X_AUTHENTICATION=self._create_authentication_header(self.test_uuid))
        self.assertEqual(response.status_code, 403)

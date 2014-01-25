"""Glue between OpenID and django.contrib.auth."""
from models import UserGoogleID, CredentialsModel
import httplib2
from apiclient.discovery import build
from oauth2client.django_orm import Storage
__metaclass__ = type
from django.contrib.auth.models import User
import conf

class GoogleAuthBackend:
    """A django.contrib.auth backend that authenticates the user based on
    an google response."""

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, **kwargs):
        credentials = kwargs.get('credentials_obj')
        if credentials is None:
            return None

#        if credentials.status != SUCCESS:
#            return None

        http = httplib2.Http()
        http = credentials.authorize(http)
        service = build('plus', 'v1', http=http)
        people_resource = service.people()
        user_details = people_resource.get(userId='me').execute()
        user = None
        try:
            user_openid = UserGoogleID.objects.get(
                googleplus_id__exact=user_details.get('id'))
        except UserGoogleID.DoesNotExist:
            if conf.CREATE_USERS:
                email = user_details.get('emails')[0].get('value')
                domain = email.split('@')[1]
                if not conf.CREATE_GMAIL_USERS and domain == "gmail.com":
                    return None
                user = self.create_user_from_google(user_details, credentials)
        else:
            user = user_openid.user

        if user is None:
            return None

        details = self._extract_user_details(user_details)
        if details:
            self.update_user_details(user, details)

        return user

    def _extract_user_details(self, user_details):
        first_name = user_details.get('name').get('familyName')
        last_name = user_details.get('name').get('givenName')
        email = user_details.get('emails')[0].get('value')
        return dict(email=email,
                    first_name=first_name, last_name=last_name)

    def create_user_from_google(self, user_details, credentials):
        details = self._extract_user_details(user_details)
        nickname = details.get('nickname') or 'openiduser'
        email = details['email'] or ''

        # Pick a username for the user based on their nickname,
        # checking for conflicts.
        i = 1
        while True:
            username = nickname
            if i > 1:
                username += str(i)
            try:
                User.objects.get(username__exact=username)
            except User.DoesNotExist:
                break
            i += 1

        user = User.objects.create_user(username, email, password=None)
        self.update_user_details(user, details)
        UserGoogleID.objects.create(
                googleplus_id=user_details.get('id'), user=user)
        domain = user.email.split('@')[1]
        if conf.STORE_CREDENTIALS:
            if domain == 'gmail.com' and conf.STORE_GMAIL_USER_CREDENTIALS:
                self.associate_credentials(user, credentials)
            elif conf.STORE_GOOGLE_APPS_USER_CREDENTIALS:
                self.associate_credentials(user, credentials)
        return user

    def associate_credentials(self, user, credentials):
        storage = Storage(CredentialsModel, 'id', user, 'credential')
        storage.put(credentials)


    def update_user_details(self, user, details):
        updated = False
        if details['first_name']:
            user.first_name = details['first_name']
            updated = True
        if details['last_name']:
            user.last_name = details['last_name']
            updated = True
        if details['email']:
            user.email = details['email']
            updated = True

        if updated:
            user.save()


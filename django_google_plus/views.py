from django.conf import settings
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, authenticate, login as auth_login)
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from oauth2client.client import FlowExchangeError, OAuth2WebServerFlow
#    flow_from_clientsecrets
import conf

conf.GOOGLE_CLIENT_SECRET = "ExIY6cALk7pLiMgjwI5e1cLP"
conf.GOOGLE_CLIENT_ID = "417231516741-8sc7fgf5u3df29iferkjivglltrd9jaj.apps.googleusercontent.com"
flow = OAuth2WebServerFlow(client_id=conf.GOOGLE_CLIENT_ID,
                           client_secret=conf.GOOGLE_CLIENT_SECRET,
                           scope='https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email',
                           redirect_uri='http://example.com/auth_return')
#CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')
#flow = flow_from_clientsecrets(
#        CLIENT_SECRETS,
#        scope='https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email')


def default_render_failure(request, message, status=403,
                           template_name='google_plus/failure.html'):
    """Render an error page to the user."""
    data = render_to_string(
        template_name, dict(message=message),
        context_instance=RequestContext(request))
    return HttpResponse(data, status=status)


@csrf_exempt
def login_begin(request, template_name='google_plus/login.html',
                redirect_uri=None,
                domain='iserviceglobe.net',
                scopes=None,
                render_failure=default_render_failure):

    if request.user.is_authenticated():
        return HttpResponseRedirect('/home')

    if 'error' in request.GET:
        return render_failure(request, 'access_denied')

    if request.method == "POST":
        try:
            redirect_uri = 'http://127.0.0.1:8000/complete'
            if flow.client_id is None and flow.client_secret is None:
                return render_failure(request, 'client_id and client secret required')
            if domain is not None:
                flow.hd = domain
            if scopes is not None:
                flow.scope = scopes
            auth_uri = flow.step1_get_authorize_url(redirect_uri=redirect_uri)
            return HttpResponseRedirect(auth_uri)
        except FlowExchangeError:
            return render_failure(request, 'Error')
    c = RequestContext(request, {})
    return render_to_response(template_name, context_instance=c)


@csrf_exempt
def login_complete(request, redirect_field_name=REDIRECT_FIELD_NAME,
                   render_failure=default_render_failure):
    code = request.GET.get('code')
    credentials = flow.step2_exchange(code)
    domain = credentials.id_token.get('hd', None)
    user = authenticate(credentials_obj=credentials)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            return HttpResponseRedirect('/home')
        else:
            return render_failure(request, 'Disabled account')
    else:
        return render_failure(request, 'Unknown user')


@csrf_exempt
def welcome(request, template_name='google_plus/welcome.html'):
    c = RequestContext(request, {})
    return render_to_response(template_name, context_instance=c)

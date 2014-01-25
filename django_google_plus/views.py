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
conf.GOOGLE_REDIRECT_URI = 'http://127.0.0.1:8000/openid/complete'
flow = OAuth2WebServerFlow(client_id=conf.GOOGLE_CLIENT_ID,
                           client_secret=conf.GOOGLE_CLIENT_SECRET,
                           scope='https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email',
                           redirect_uri=conf.GOOGLE_REDIRECT_URI)
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
                domain=None,
                scopes=None,
                redirect_field_name=REDIRECT_FIELD_NAME,
                render_failure=default_render_failure):

    redirect_to = request.REQUEST.get(redirect_field_name, '')
    request.session['next'] = redirect_to

    if 'error' in request.GET:
        return render_failure(request, 'access_denied')

    try:
        if flow.client_id is None:
            return render_failure(request, 'client_id required')
        if flow.client_secret is None:
            return render_failure(request, 'client secret required')
        if flow.redirect_uri is None:
            return render_failure(request, 'redirect uri required')
        if domain is not None:
            flow.hd = domain
        if scopes is not None:
            flow.scope = scopes
        auth_uri = flow.step1_get_authorize_url()
        return HttpResponseRedirect(auth_uri)
    except FlowExchangeError:
        return render_failure(request, 'Error')


@csrf_exempt
def login_complete(request, redirect_field_name=REDIRECT_FIELD_NAME,
                   render_failure=default_render_failure):

    redirect_to = request.session.get('next')

    code = request.GET.get('code')
    credentials = flow.step2_exchange(code)
#    domain = credentials.id_token.get('hd', None)
    user = authenticate(credentials_obj=credentials)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            return HttpResponseRedirect(redirect_to)
        else:
            return render_failure(request, 'Disabled account')
    else:
        return render_failure(request, 'Unknown user')


@csrf_exempt
def welcome(request, template_name='google_plus/welcome.html'):
    c = RequestContext(request, {})
    return render_to_response(template_name, context_instance=c)

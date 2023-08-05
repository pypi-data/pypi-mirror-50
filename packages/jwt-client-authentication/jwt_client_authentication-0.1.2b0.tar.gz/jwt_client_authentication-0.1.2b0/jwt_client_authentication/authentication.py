import logging

from .settings import settings

from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework import exceptions, status
from django.contrib.auth import get_user_model, authenticate

import requests
import jwt

class jwt(TokenAuthentication):
    def authenticate(self, request):
        print "request received"
        token = get_authorization_header(request)
        try:
            token = token.split(' ')[-1]
            if not token:
                token = request.query_params.get('token')
        except:
            pass
        return self.authenticate_token(token)

    def authenticate_token(self, token):
        rr = requests.post(settings.get('CAS_URL') + "/api-token-verify/", data={
            "token": token
        })
        if rr.status_code in (200, 201):
            resp = rr.json()
            print "CAS did authenticate user %s" % resp["user"]["username"]
            user = get_user_model().objects.get_or_create(
                username=resp['user']['username'])
            return user
        else:
            raise exceptions.AuthenticationFailed(
                'You have no access to this application')

def getTokenContent(f):
    def wrapper(item, request, *args, **kwargs):
        token = get_authorization_header(request)
        try:
            token = token.split(" ")[-1]
            if not token:
                token = request.query_params.get("token")
        except: return status.HTTP_401_UNAUTHORIZED
            
        decrypted = jwt.decode(token, verify=False)
        if "allowed_ids" in decrypted:
            f(item, request, *args, allowed_ids=allowed_ids, **kwargs)
        else:
            return status.HTTP_401_UNAUTHORIZED
    return wrapper
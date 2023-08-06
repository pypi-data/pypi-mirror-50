from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.db.models import Q
from ohm2_handlers_light import utils as h_utils
from ohm2_handlers_light.definitions import RunException
from . import models as matialvarezs_node_accounts_models
from . import errors as matialvarezs_node_accounts_errors
from . import settings
import os, time, random
from rest_framework.authtoken.models import Token

random_string = "zloqiE64VHxcTTcydOgGukTyRnqvsAkt"



"""
def parse_model_attributes(**kwargs):
	attributes = {}
	
	return attributes

def create_model(**kwargs):

	for key, value in parse_model_attributes(**kwargs).items():
		kwargs[key] = value
	return h_utils.db_create(matialvarezs_node_accounts_models.Model, **kwargs)

def get_model(**kwargs):
	return h_utils.db_get(matialvarezs_node_accounts_models.Model, **kwargs)

def get_or_none_model(**kwargs):
	return h_utils.db_get_or_none(matialvarezs_node_accounts_models.Model, **kwargs)

def filter_model(**kwargs):
	return h_utils.db_filter(matialvarezs_node_accounts_models.Model, **kwargs)

def q_model(q, **otions):
	return h_utils.db_q(matialvarezs_node_accounts_models.Model, q)

def delete_model(entry, **options):
	return h_utils.db_delete(entry)

def update_model(entry, **kwargs):
	attributes = {}
	for key, value in parse_model_attributes(**kwargs).items():
		attributes[key] = value
	return h_utils.db_update(entry, **attributes)
"""
def get_or_none_user(**kwargs):
    return h_utils.db_get_or_none(User, **kwargs)


def create_user(**kwargs):
    return h_utils.db_create(User, **kwargs)


def get_or_none_token(**kwargs):
    return h_utils.db_get_or_none(Token, **kwargs)


def create_token(**kwargs):
    return h_utils.db_create(Token, **kwargs)


def create_user_api_if_not_exist_and_return_token():
    user = get_or_none_user(username='api')
    if not user:
        user = create_user(username='api', email='', password='apinodesisnbyted')
        token = create_token(user=user)
        return token
    token = get_or_none_token(user=user)
    return token

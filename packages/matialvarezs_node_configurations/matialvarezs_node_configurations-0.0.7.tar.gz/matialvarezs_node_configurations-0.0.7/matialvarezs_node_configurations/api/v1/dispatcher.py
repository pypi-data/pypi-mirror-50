from .decorators import api_v1_safe_request
from ohm2_handlers_light import utils as h_utils
from django.contrib.auth.models import User
import binascii
from . import errors as api_v1_errors
from configuration import utils as configuration_utils
from accounts import utils as accounts_utils


@api_v1_safe_request
def create_identity(request, params):
    config = configuration_utils.create_configuration(key='identity', value=params['identity'])
    token_user_api = accounts_utils.create_user_api_if_not_exist_and_return_token()
    ret = {
        "token_user_api": token_user_api.key
    }
    return ret

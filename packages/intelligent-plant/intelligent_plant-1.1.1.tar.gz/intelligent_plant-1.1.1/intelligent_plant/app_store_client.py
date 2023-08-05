"""This module implments a client for the Intelligent Plant App Store API"""
__author__ = "Ross Kelso"
__docformat__ = 'reStructuredText'

import urllib

import requests

import intelligent_plant.data_core_client as data_core_client
import intelligent_plant.http_client as http_client

class AppStoreClient(http_client.HttpClient):
    """Access the Intelligent Plant Appstore API"""

    def __init__(self, access_token, refresh_token=None, base_url = "https://appstore.intelligentplant.com/"):
        """
        Initialise an App Store Client
        :param access_token: The access token used to authenticate this client. 
            Get this by using the authorization code c#grant flow (for web servers) or
            the implicit grant flow (for clients e.g. native apps, JS web clients, Jupyter Notebook)
            Examples of this can be found in the "examples" folder and Jupyter notebook.
        :param refresh_token: The refresh token for this client (currently unused).
        :param base_url: The URL of the app store (optional, default value is "https://appstore.intelligentplant.com/").

        :return: An app store client that uses the provided access token for authorization.
        """
        self.access_token = access_token
        self.refresh_token = refresh_token

        http_client.HttpClient.__init__(self, "Bearer " + self.access_token, base_url)

    def get_data_core_client(self, data_core_url = None):
        """
        Get the data core client with the same authorization details as this app store client.
        :param data_core_url: The base URL for the data core API (optional, leaving it unspecified will determine the data core url relative to this client's base URL)

        :return: The data core client with the same authorization as this app store client.
        """
        data_core_url = urllib.parse.urljoin(self.base_url, "gestalt/") if data_core_url == None else data_core_url
        return data_core_client.DataCoreClient("Bearer " + self.access_token, base_url = data_core_url)

    def get_user_info(self):
        """
        Get the authenticated user's user info from the app store.

        :return: The users infor as a parsed JSON object
        :raises: :class:`HTTPError`, if one occurred.
        :raises: An exception if JSON decoding fails.
        """
        return self.get_json("api/resource/userinfo")

    def get_user_balance(self):
        """
        Get the authenticated user's balance of credits.

        :return: The users balance as a float
        :raises: :class:`HTTPError`, if one occurred.
        """
        return float(self.get_text("api/resource/userbalance"))

    def debit_account(self, amount):
        """
        Debit the user's app store account.
        :param amount: The number of credits that should be debited from the user's account.

        :return: The transaction reference of the user's payment.
        :raises: :class:`HTTPError`, if one occurred.
        :raises: An exception if JSON decoding fails.
        """
        params = {
            "debitAmount": amount
        }

        return self.post_json("api/resource/debit", params=params)

    def refund_account(self, transaction_ref):
        """
        Refund a transaction
        :param transaction_ref: The transaction reference of the transation you want to refund.

        :return: The requests response object.
        :raises: :class:`HTTPError`, if one occurred.
        """

        params = {
            "transactionRef": transaction_ref
        }

        return self.post("api/resource/refund", params=params)

def get_authorization_code_grant_flow_url(app_id, redirect_uri, scopes, base_url = "https://appstore.intelligentplant.com"):
    """
    Get the url that the client should use for authorization code grant flow
    This grant flow should be used by web servers as it requires the app secret (which should not be made public).
    For information on the authorisation flow see: https://appstore.intelligentplant.com/wiki/doku.php?id=dev:app_store_developers
    :param app_id: The ID of the app to authenticate under (found under Developer > Applications > Settings on the app store)
    :param redirect_uri: The URI to redirect the user to after they log in with the authentication token (must be an authorized redirect URI in the app developer settings)
    :param scopes: A list of string that are the scopes the user is granting (e.g. "UserInfo" and "DataRead")
    :param base_url: The app store base url (optional, default value is "https://appstore.intelligentplant.com")

    :return: The URL that the user should be redirected to to log in.
    """
    params = {
        'response_type': "code",
        'client_id': app_id,
        'redirect_uri': redirect_uri,
        'scope': " ".join(scopes)
    }
    url = base_url + "/authorizationserver/oauth/authorize?" + urllib.parse.urlencode(params)

    return url

def complete_authorization_code_grant_flow(auth_code, app_id, app_secret, redirect_uri, base_url = "https://appstore.intelligentplant.com"):
    """
    Complete logging in the user using authroization grant flow
    This grant flow should be used by web servers as it requires the app secret (which should not be made public).
    For information on the authorisation flow see: https://appstore.intelligentplant.com/wiki/doku.php?id=dev:app_store_developers
    :param auth_code: The code that was returned to the redirect URI after the user logged in.
    :param app_id: The ID of the app to authenticate under (found under Developer > Applications > Settings on the app store)
    :param app_secret: The secret of the app to authenticate under (found under Developer > Applications > Settings on the app store) :warn This should not be published.
    :param redirect_uri: Sn authorized redirect URI in the app developer settings
    :param base_url: The app store base url (optional, default value is "https://appstore.intelligentplant.com")

    :return: An app store client with the access token specified
    """
    url = base_url + "/authorizationserver/oauth/token"

    params = {
        'grant_type': "authorization_code",
        'code': auth_code,
        'client_id': app_id,
        'client_secret': app_secret,
        'redirect_uri': redirect_uri
    }
    
    r = requests.post(url, params)

    if (r.status_code == requests.codes.ok):
        token = r.json()

        return AppStoreClient(token['access_token'], None)
    else:
        r.raise_for_status()

    
def get_implicit_grant_flow_url(app_id, redirect_url, scopes, base_url = "https://appstore.intelligentplant.com"):
    """
    Get the url that the client should use for implicit grant flow.
    This grant flow should be used by native applications and clients, as it doesn't require the app secret.
    For information on the authorisation flow see: https://appstore.intelligentplant.com/wiki/doku.php?id=dev:app_store_developers
    :param app_id: The ID of the app to authenticate under (found under Developer > Applications > Settings on the app store)
    :param redirect_url: The URL to redirect the user to after they log in with the access token (must be an authorized redirect URI in the app developer settings)
    :param scopes: A list of string that are the scopes the user is granting (e.g. "UserInfo" and "DataRead")
    :param base_url: The app store base url (optional, default value is "https://appstore.intelligentplant.com")

    :return: The URL that the user should be redirected to to log in.
    """
    params = {
        'response_type': "token",
        'client_id': app_id,
        'redirect_uri': redirect_url,
        'scope': " ".join(scopes)
    }

    url = base_url + "/authorizationserver/oauth/authorize?" + urllib.parse.urlencode(params)

    return url



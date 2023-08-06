import os
import requests


class EloquaSession:
    """ Test Eloqua Session class"""

    def __init__(self, company=None, username=None, password=None):
        """
        Logs into Eloqua API and configures default request parameters

        :param company: Eloqua company
        :param username: Eloqua login username
        :param password: Eloqua login password
        """

        if company is None:
            company = os.environ["ELOQUA_COMPANY"]
        if username is None:
            username = os.environ["ELOQUA_USER"]
        if password is None:
            password = os.environ["ELOQUA_PASSWORD"]

        self.login_url = "https://login.eloqua.com/id"
        self.headers = {"Content-Type": "application/json"}
        self.api_version = "1.0"
        self.auth = ("{}\{}".format(company, username), password)

        req = requests.get(self.login_url, auth=self.auth)

        self.url_base = req.json()["urls"]["base"]

    def get(self, url, *args, **kwargs) -> requests.Response:
        """
        HTTP GET method, inserts default values and base url

        :param url: Eloqua URL endpoint
        :param args: any additional args
        :param kwargs: any additional kwargs
        :return: (requests.Response) HTTP Response
        """
        full_url = "{}{}".format(self.url_base, url)
        return requests.get(full_url, *args, auth=self.auth, **kwargs)

    def post(self, url, *args, **kwargs) -> requests.Response:
        """
        HTTP POST method, inserts default values and base url

        :param url: Eloqua URL endpoint
        :param args: any additional args
        :param kwargs: any additional kwargs
        :return: (requests.Response) HTTP Response
        """
        full_url = "{}{}".format(self.url_base, url)
        return requests.post(
            full_url, *args, auth=self.auth, headers=self.headers, **kwargs
        )

    def put(self, url, *args, **kwargs) -> requests.Response:
        """
        HTTP GET method, inserts default values and base url

        :param url: Eloqua URL endpoint
        :param args: any additional args
        :param kwargs: any additional kwargs
        :return: (requests.Response) HTTP Response
        """
        full_url = "{}{}".format(self.url_base, url)
        return requests.put(
            full_url, *args, auth=self.auth, headers=self.headers, **kwargs
        )

    def delete(self, url, *args, **kwargs) -> requests.Response:
        """
        HTTP DELETE method, inserts default values and base url

        :param url: Eloqua URL endpoint
        :param args: any additional args
        :param kwargs: any additional kwargs
        :return: (requests.Response) HTTP Response
        """
        full_url = "{}{}".format(self.url_base, url)

        if "headers" not in kwargs:
            kwargs["headers"] = self.headers
        if "auth" not in kwargs:
            kwargs["auth"] = self.auth

        return requests.delete(full_url, *args, **kwargs)
